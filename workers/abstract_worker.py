__author__ = 'Bohdan Mushkevych'

from settings import settings
from system.performance_tracker import SimpleTracker
from system.synergy_process import SynergyProcess

from threading import Thread


class AbstractWorker(SynergyProcess):
    def __init__(self, process_name, process_id=None):
        """:param process_name: id of the process, the worker will be performing """
        super(AbstractWorker, self).__init__(process_name, process_id)
        self._init_performance_tracker(self.logger)

        msg_suffix = 'Testing Mode' if settings['under_test'] else 'Production Mode'
        self.logger.info('Started {0} in {1}'.format(self.process_name, msg_suffix))

    def __del__(self):
        try:
            self.performance_tracker.cancel()
        except Exception as e:
            self.logger.error('Exception caught while cancelling the performance_tracker: {0}'.format(str(e)))
        super(AbstractWorker, self).__del__()

    # ********************** abstract methods ****************************
    def _init_performance_tracker(self, logger):
        self.performance_tracker = SimpleTracker(logger)
        self.performance_tracker.start()
        
    # ********************** thread-related methods ****************************
    def run(self):
        """ abstract method to be overridden in children classes """
        self.logger.info('Thread started')

    def start(self, *_):
        self.main_thread = Thread(target=self.run)
        self.main_thread.start()
