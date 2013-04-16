"""
Created on 2011-03-11

@author: Bohdan Mushkevych
"""
import os

from system.data_logging import Logger
from settings import settings

TYPE_ALERT = 'type_alert'
TYPE_HORIZONTAL_AGGREGATOR = 'type_horizontal'
TYPE_VERTICAL_AGGREGATOR = 'type_vertical'
TYPE_GARBAGE_COLLECTOR = 'type_gc'

PROCESS_GC = 'GarbageCollectorWorker'
PROCESS_SITE_HOURLY = 'SiteHourlyAggregator'
PROCESS_ALERT_DAILY = 'AlertDailyWorker'

_TOKEN_SCHEDULER = 'scheduler'
_TOKEN_GC = 'gc'
_TOKEN_SITE = 'site'
_TOKEN_ALERT = 'alert'

_ROUTING_PREFIX = 'routing_'
_QUEUE_PREFIX = 'queue_'
_VOID = 'VOID'

_NAME = 'process_name'
_LOG_FILENAME = 'log_filename'
_LOG_TAG = 'log_tag'
_PID_FILENAME = 'pid_filename'
_CLASSNAME = 'classname'
_SOURCE_COLLECTION = 'source_collection'
_TARGET_COLLECTION = 'target_collection'
_MQ_QUEUE = 'mq_queue'
_MQ_EXCHANGE = 'mq_exchange'
_MQ_ROUTING_KEY = 'mq_routing_key'
_TIME_QUALIFIER = 'time_qualifier'
_TYPE = 'type'

def _create_context_entry(process_name,
                          classname,
                          token,
                          time_qualifier,
                          exchange,
                          queue=None,
                          routing=None,
                          type=None,
                          source_collection=_VOID,
                          target_collection=_VOID,
                          pid_file=None,
                          log_file=None):
    """ forms process context entry """
    if queue is None:
        queue = _QUEUE_PREFIX + token + time_qualifier
    if routing is None:
        routing = _ROUTING_PREFIX + token + time_qualifier
    if pid_file is None:
        pid_file = token + time_qualifier + '.pid'
    if log_file is None:
        log_file = token + time_qualifier + '.log'

    return {
        _NAME: process_name,
        _PID_FILENAME: settings['pid_directory'] + pid_file,
        _CLASSNAME: classname,
        _LOG_FILENAME: settings['log_directory'] + log_file,
        _LOG_TAG: token + time_qualifier,
        _SOURCE_COLLECTION: source_collection,
        _TARGET_COLLECTION: target_collection,
        _MQ_QUEUE: queue,
        _MQ_EXCHANGE: exchange,
        _MQ_ROUTING_KEY: routing,
        _TIME_QUALIFIER: time_qualifier,
        _TYPE: type
    }


class ProcessContext:
    # process_context format: "process_name": {
    # process_name
    # log_filename
    # log_tag
    # pid_filename
    # full_classname
    # source_collection
    # target_collection
    # mq_queue
    # mq_exchange
    # mq_routing_key
    # time_qualifier
    # type
    # }

    QUEUE_RAW_DATA = 'queue_raw_data'
    ROUTING_IRRELEVANT = 'routing_irrelevant'

    QUALIFIER_REAL_TIME = '_real_time'
    QUALIFIER_BY_SCHEDULE = '_by_schedule'
    QUALIFIER_HOURLY = '_hourly'
    QUALIFIER_DAILY = '_daily'
    QUALIFIER_MONTHLY = '_monthly'
    QUALIFIER_YEARLY = '_yearly'

    EXCHANGE_RAW_DATA = 'exchange_raw_data'
    EXCHANGE_VERTICAL = 'exchange_vertical'
    EXCHANGE_HORIZONTAL = 'exchange_horizontal'
    EXCHANGE_ALERT = 'exchange_alert'
    EXCHANGE_UTILS = 'exchange_utils'

    logger_pool = dict()

    PROCESS_CONTEXT = {
        PROCESS_SITE_HOURLY: _create_context_entry(
            process_name=PROCESS_SITE_HOURLY,
            classname='workers.site_hourly_aggregator.SiteHourlyAggregator',
            token=_TOKEN_SITE,
            time_qualifier=QUALIFIER_HOURLY,
            exchange=EXCHANGE_VERTICAL,
            type=TYPE_VERTICAL_AGGREGATOR,
            source_collection= 'single_session_collection'),
        PROCESS_GC: _create_context_entry(
            process_name=PROCESS_GC,
            classname='workers.garbage_collector_worker.GarbageCollectorWorker',
            token=_TOKEN_GC,
            time_qualifier=QUALIFIER_BY_SCHEDULE,
            exchange=EXCHANGE_UTILS,
            type=TYPE_GARBAGE_COLLECTOR,
            source_collection='units_of_work_collection',
            target_collection='units_of_work_collection'),

        PROCESS_ALERT_DAILY: _create_context_entry(
            process_name=PROCESS_ALERT_DAILY,
            classname='workers.hadoop_aggregator_driver.HadoopAggregatorDriver',
            token=_TOKEN_ALERT,
            time_qualifier=QUALIFIER_DAILY,
            exchange=EXCHANGE_ALERT,
            type=TYPE_HORIZONTAL_AGGREGATOR),

        'TestAggregator': _create_context_entry(
            process_name='TestAggregator',
            classname='',
            token='test',
            time_qualifier='',
            exchange=''),
    }

    @classmethod
    def create_pid_file(cls, process_name):
        """ creates pid file and writes os.pid() in there """
        pid_filename = cls.get_pid_filename(process_name)
        try:
            pid_file = open(pid_filename, mode='w')
            pid_file.write(str(os.getpid()))
        except Exception as e:
            cls.get_logger(process_name).error('Unable to create pid file at: %s, because of: %r' % (pid_filename, e))

    @classmethod
    def remove_pid_file(cls, process_name):
        """ removes pid file """
        pid_filename = cls.get_pid_filename(process_name)
        try:
            os.remove(pid_filename)
            cls.get_logger(process_name).info('Removed pid file at: %s' % pid_filename)
        except Exception as e:
            cls.get_logger(process_name).error('Unable to remove pid file at: %s, because of: %r' % (pid_filename, e))

    @classmethod
    def get_logger(cls, process_name):
        """ method returns initiated logger"""
        if process_name not in cls.logger_pool:
            file_name = cls.get_log_filename(process_name)
            tag = cls.get_log_tag(process_name)
            cls.logger_pool[process_name] = Logger(file_name, tag)
        return cls.logger_pool[process_name].get_logger()

    @classmethod
    def get_record(cls, process_name):
        """ method returns dictionary of strings, preset
        source collection, target collection, queue name, exchange, routing, etc"""
        return cls.PROCESS_CONTEXT[process_name]

    @classmethod
    def get_pid_filename(cls, process_name):
        """method returns path for the PID FILENAME """
        return cls.PROCESS_CONTEXT[process_name][_PID_FILENAME]

    @classmethod
    def get_classname(cls, process_name):
        """ method returns fully qualified classname of the instance running as process"""
        return cls.PROCESS_CONTEXT[process_name][_CLASSNAME]

    @classmethod
    def get_log_filename(cls, process_name):
        """method returns path for the Log filename"""
        return cls.PROCESS_CONTEXT[process_name][_LOG_FILENAME]

    @classmethod
    def get_log_tag(cls, process_name):
        """method returns tag that all logging messages will be marked with"""
        return cls.PROCESS_CONTEXT[process_name][_LOG_TAG]

    @classmethod
    def get_time_qualifier(cls, process_name):
        """ method returns worker/aggregator time scale (like daily or yearly)"""
        return cls.PROCESS_CONTEXT[process_name][_TIME_QUALIFIER]

    @classmethod
    def get_routing(cls, process_name):
        """ method returns routing; it is used to segregate traffic within the queue
        for instance: routing_hourly for hourly reports, while routing_yearly for yearly reports"""
        return cls.PROCESS_CONTEXT[process_name][_MQ_ROUTING_KEY]

    @classmethod
    def get_exchange(cls, process_name):
        """ method returns exchange for this classname.
        Exchange is a component that sits between queue and the publisher"""
        return cls.PROCESS_CONTEXT[process_name][_MQ_EXCHANGE]

    @classmethod
    def get_queue(cls, process_name):
        """ method returns queue that is applicable for the worker/aggregator, specified by classname"""
        return cls.PROCESS_CONTEXT[process_name][_MQ_QUEUE]

    @classmethod
    def get_target_collection(cls, process_name):
        """ method returns target collection - the one where aggregated data will be placed in """
        return cls.PROCESS_CONTEXT[process_name][_TARGET_COLLECTION]

    @classmethod
    def get_source_collection(cls, process_name):
        """ method returns source collection - the one where data is taken from for analysis"""
        return cls.PROCESS_CONTEXT[process_name][_SOURCE_COLLECTION]

    @classmethod
    def get_type(cls, process_name):
        """ method returns process type
        Supported types are listed in process_context starting with TYPE_ prefix and are enumerated in
        scheduler.start() method"""
        return cls.PROCESS_CONTEXT[process_name][_TYPE]

if __name__ == '__main__':
    pass