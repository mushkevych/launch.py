__author__ = 'Bohdan Mushkevych'

import setproctitle

from settings import settings
from system.process_context import ProcessContext

class SynergyProcess(object):
    """ Fundamental class for all processes. Registers logger and renames process to SynergyYYY"""

    def __init__(self, process_name, process_id=None):
        """ renames process to SynergyYYY and creates PID file """
        self.process_name = process_name
        self.process_id = process_id
        self.logger = ProcessContext.get_logger(process_name, process_id=self.process_id)

        # process-related activities
        process_title = settings['process_prefix'] + self.process_name
        if self.process_id:
            process_title += self.process_id
        setproctitle.setproctitle(process_title)
        ProcessContext.create_pid_file(self.process_name, process_id=self.process_id)

    def __del__(self):
        """ removes PID file """
        ProcessContext.remove_pid_file(self.process_name, process_id=self.process_id)
        self.logger.info('Shutdown {0}'.format(self.process_name))
