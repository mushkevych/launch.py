__author__ = 'Bohdan Mushkevych'

from settings import settings
from system.performance_tracker import SimpleTracker
from system.synergy_process import SynergyProcess

from threading import Thread


class AbstractWorker(SynergyProcess):
    def __init__(self, process_name):
        """:param process_name: id of the process, the worker will be performing """
        super(AbstractWorker, self).__init__(process_name)
        self._init_performance_ticker(self.logger)

        msg_suffix = 'in Production Mode'
        if settings['under_test']:
            msg_suffix = 'in Testing Mode'
        self.logger.info('Started %s %s' % (self.process_name, msg_suffix))

    def __del__(self):
        try:
            self.performance_ticker.cancel()
        except Exception as e:
            self.logger.error('Exception caught while cancelling the performance_ticker: %s' % str(e))
        super(AbstractWorker, self).__del__()

    # ********************** abstract methods ****************************
    def _init_performance_ticker(self, logger):
        self.performance_ticker = SimpleTracker(logger)
        self.performance_ticker.start()
        
    # ********************** thread-related methods ****************************
    def run(self):
        """ abstract method to be overridden in children classes """
        self.logger.info('Thread started')

    def start(self, *args):
        self.main_thread = Thread(target=self.run)
        self.main_thread.start()
