"""
Created on 2011-02-01

@author: Bohdan Mushkevych
"""

from settings import settings
from system.performance_ticker import WorkerPerformanceTicker
from system.synergy_process import SynergyProcess

from threading import Thread


class AbstractWorker(SynergyProcess):
    """
    class works as an abstract basement for all workers and aggregators
    """

    def __init__(self, process_name):
        """@param process_name: id of the process, the worker will be performing """
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
        self.performance_ticker = WorkerPerformanceTicker(logger)
        self.performance_ticker.start()
        
    # ********************** thread-related methods ****************************
    def run(self):
        """ abstract method to be overridden in children classes """
        pass

    def start(self):
        self.main_thread = Thread()
        self.main_thread.start()
