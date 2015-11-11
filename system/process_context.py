__author__ = 'Bohdan Mushkevych'

import os

from system.system_logger import Logger
from settings import settings

# User fields

# Framework fields
_NAME = 'process_name'
_LOG_FILENAME = 'log_filename'
_LOG_TAG = 'log_tag'
_PID_FILENAME = 'pid_filename'
_CLASSNAME = 'classname'


def _create_context_entry(process_name,
                          classname,
                          token,
                          pid_file=None,
                          log_file=None):
    """ forms process context entry """
    pid_file = pid_file if pid_file is not None else '{0}.pid'.format(token)
    log_file = log_file if log_file is not None else '{0}.log'.format(token)

    return {
        _NAME: process_name,
        _PID_FILENAME: os.path.join(settings['pid_directory'], pid_file),
        _CLASSNAME: classname,
        _LOG_FILENAME: os.path.join(settings['pid_directory'], log_file),
        _LOG_TAG: token,
    }


class ProcessContext(object):
    # format: "process_name": {
    #     process_name
    #     pid_filename
    #     classname
    #     log_filename
    #     log_tag
    #     time_qualifier
    # }
    CONTEXT = {
    }

    # format: {"process_name" : system_logger.Logger}
    LOGGER_POOL = dict()

    @classmethod
    def create_pid_file(cls, process_name, process_id=None):
        """ creates pid file and writes os.pid() in there """
        pid_filename = cls.get_pid_filename(process_name, process_id)
        try:
            with open(pid_filename, mode='w') as pid_file:
                pid_file.write(str(os.getpid()))
        except Exception as e:
            cls.get_logger(process_name).error('Unable to create pid file at: {0}, because of: {1}'.
                                               format(pid_filename, e))

    @classmethod
    def remove_pid_file(cls, process_name, process_id=None):
        """ removes pid file """
        pid_filename = cls.get_pid_filename(process_name, process_id)
        try:
            os.remove(pid_filename)
            cls.get_logger(process_name).info('Removed pid file at: {0}'.format(pid_filename))
        except Exception as e:
            cls.get_logger(process_name).error('Unable to remove pid file at: {0}, because of: {1}'.
                                               format(pid_filename, e))

    @classmethod
    def get_logger(cls, process_name, process_id=None):
        """ method returns initiated logger"""
        if process_name not in cls.LOGGER_POOL:
            file_name = cls.get_log_filename(process_name)
            tag = cls.get_log_tag(process_name)
            cls.LOGGER_POOL[process_name] = Logger(file_name, tag)

        logger = cls.LOGGER_POOL[process_name].get_logger()
        if process_id:
            return logger.getChild(str(process_id))
        else:
            return logger

    @classmethod
    def get_record(cls, process_name):
        """ method returns dictionary of strings, preset
        source collection, target collection, queue name, exchange, routing, etc"""
        return cls.CONTEXT[process_name]

    @classmethod
    def get_pid_filename(cls, process_name, process_id=None):
        """method returns path for the PID FILENAME """
        pid_filename = cls.CONTEXT[process_name][_PID_FILENAME]
        if process_id:
            pid_filename = pid_filename[:-4] + str(process_id) + pid_filename[-4:]
        return pid_filename

    @classmethod
    def get_classname(cls, process_name):
        """ method returns fully qualified classname of the instance running as process"""
        return cls.CONTEXT[process_name][_CLASSNAME]

    @classmethod
    def get_log_filename(cls, process_name):
        """method returns path for the Log filename"""
        return cls.CONTEXT[process_name][_LOG_FILENAME]

    @classmethod
    def get_log_tag(cls, process_name):
        """method returns tag that all logging messages will be marked with"""
        return cls.CONTEXT[process_name][_LOG_TAG]


if __name__ == '__main__':
    pass
