__author__ = 'Bohdan Mushkevych'

import time
import os

import psutil

from system.repeat_timer import RepeatTimer
from settings import settings


class FootprintCalculator(object):
    def __init__(self):
        self.pid = os.getpid()

    def group(self, number):
        """ method formats number and inserts thousands separators """
        s = '%d' % number
        groups = []
        while s and s[-1].isdigit():
            groups.append(s[-3:])
            s = s[:-3]
        return s + '\''.join(reversed(groups))

    def get_snapshot_as_list(self):
        ps = psutil.Process(self.pid)
        return (self.group(ps.get_memory_info()[0]),
                self.group(ps.get_memory_info()[1]),
                '%02d' % ps.get_cpu_percent(),
                self.group(psutil.phymem_usage().free),
                self.group(psutil.virtmem_usage().free))

    def get_snapshot(self):
        resp = 'Footprint: RSS=%r VMS=%r CPU=%r; Available: PHYS=%r VIRT=%r' % self.get_snapshot_as_list()
        return resp


class Tracker(object):
    def __init__(self, name):
        self.name = name
        self.per_24h = 0
        self.per_tick = 0

    def increment(self, delta=1):
        self.per_24h += delta
        self.per_tick += delta

    def reset_tick(self):
        self.per_tick = 0

    def reset_24h(self):
        self.per_24h = 0


class TrackerPair(object):
    def __init__(self, name, up_name='Success', down_name='Failure'):
        self.name = name
        self.tracker_up = Tracker(down_name)
        self.tracker_down = Tracker(up_name)

    def increment_up(self):
        self.tracker_down.increment()

    def increment_down(self):
        self.tracker_up.increment()

    def reset_tick(self):
        self.tracker_up.reset_tick()
        self.tracker_down.reset_tick()

    def reset_24h(self):
        self.tracker_up.reset_24h()
        self.tracker_down.reset_24h()

    def to_string(self, tick_interval_seconds, show_header=True):
        header = self.name + ' : ' + self.tracker_down.name + '/' + self.tracker_up.name + '.' if show_header else ''
        return header + 'In last {0:d} seconds: {1:d}/{2:d}. In last 24 hours: {3:d}/{4:d}'.format(
            tick_interval_seconds,
            self.tracker_down.per_tick,
            self.tracker_up.per_tick,
            self.tracker_down.per_24h,
            self.tracker_up.per_24h)


class WorkerPerformanceTicker(object):
    SECONDS_IN_24_HOURS = 86400
    TICKS_BETWEEN_FOOTPRINTS = 10

    def __init__(self, logger, tracker_up_name='Success', tracker_down_name='Failure'):
        self.logger = logger
        self.tracker = TrackerPair('Processed', up_name=tracker_up_name, down_name=tracker_down_name)
        self.interval = settings['perf_ticker_interval']
        self.mark_24_hours = time.time()
        self.mark_footprint = time.time()
        self.footprint = FootprintCalculator()
        self.timer = RepeatTimer(self.interval, self._run_tick_thread)

    def start(self):
        self.timer.start()

    def cancel(self):
        self.timer.cancel()

    def is_alive(self):
        return self.timer.is_alive()

    def _print_footprint(self):
        if time.time() - self.mark_footprint > self.TICKS_BETWEEN_FOOTPRINTS * self.interval:
            self.logger.info(self.footprint.get_snapshot())
            self.mark_footprint = time.time()

    def _run_tick_thread(self):
        self._print_footprint()
        self.logger.info(self.tracker.to_string(self.interval))

        self.tracker.reset_tick()
        if time.time() - self.mark_24_hours > self.SECONDS_IN_24_HOURS:
            self.tracker.reset_24h()

    def increment_success(self):
        self.tracker.increment_up()

    def increment_failure(self):
        self.tracker.increment_down()


class SessionPerformanceTicker(WorkerPerformanceTicker):
    def __init__(self, logger):
        super(SessionPerformanceTicker, self).__init__(logger, tracker_up_name='Inserts', tracker_down_name='Updates')

    def increment_insert(self):
        super(SessionPerformanceTicker, self).increment_success()

    def increment_update(self):
        super(SessionPerformanceTicker, self).increment_failure()


class AggregatorPerformanceTicker(WorkerPerformanceTicker):
    STATE_IDLE = 'state_idle'
    STATE_PROCESSING = 'state_processing'

    def __init__(self, logger):
        super(AggregatorPerformanceTicker, self).__init__(logger)
        self.state = self.STATE_IDLE
        self.posts_per_job = 0
        self.uow_obj = None
        self.state_triggered_at = time.time()

    def _run_tick_thread(self):
        self._print_footprint()
        if self.state == self.STATE_PROCESSING or self.posts_per_tick > 0 or self.posts_per_24_hours > 0:
            msg = 'State: %s for %d sec; processed: %d in %d sec. %d in this uow; %d in 24 hours;' \
                  % (self.state,
                     time.time() - self.state_triggered_at,
                     self.posts_per_tick,
                     self.interval,
                     self.posts_per_job,
                     self.posts_per_24_hours,)
        else:
            msg = 'State: %s for %d sec;' % (self.state, time.time() - self.state_triggered_at)
        self.logger.info(msg)

        self.posts_per_tick = 0
        if time.time() - self.mark_24_hours > self.SECONDS_IN_24_HOURS:
            self.mark_24_hours = time.time()
            self.posts_per_24_hours = 0

    def increment(self):
        self.posts_per_tick += 1
        self.posts_per_24_hours += 1
        self.posts_per_job += 1

    def start_uow(self, uow_obj):
        self.state = self.STATE_PROCESSING
        self.uow_obj = uow_obj
        self.state_triggered_at = time.time()

    def finish_uow(self):
        _id = self.uow_obj.get_document()['_id']
        self.logger.info('Success: unit_of_work %s in timeperiod %s; processed %d entries in %d seconds'
                         % (_id,
                            self.uow_obj.get_timestamp(),
                            self.posts_per_job,
                            time.time() - self.state_triggered_at))
        self.cancel_uow()

    def cancel_uow(self):
        self.state = self.STATE_IDLE
        self.uow_obj = None
        self.state_triggered_at = time.time()
        self.posts_per_job = 0
