__author__ = 'Bohdan Mushkevych'

import setproctitle

from settings import settings
from system.process_context import ProcessContext

class SynergyProcess(object):
    """ Fundamental class for all processes. Registers logger and renames process to SynergyYYY"""

    def __init__(self, process_name):
        """ renames process to SynergyYYY and creates PID file """
        self.process_name = process_name
        self.logger = ProcessContext.get_logger(process_name)

        # process-related activities
        setproctitle.setproctitle(settings['process_prefix'] + self.process_name)
        ProcessContext.create_pid_file(self.process_name)

    def __del__(self):
        """ removes PID file """
        ProcessContext.remove_pid_file(self.process_name)
        self.logger.info('Shutdown {0}'.format(self.process_name))
