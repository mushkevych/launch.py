"""
Created on 2011-03-11

@author: Bohdan Mushkevych
"""
import os

from system.data_logging import Logger
from settings import settings

# User fields
PROCESS_CLASS_EXAMPLE = 'AbstractClassWorker'
PROCESS_SCRIPT_EXAMPLE = 'ScriptExampleWorker'
_TOKEN_CLASS_EXAMPLE = 'class_example'
_TOKEN_SCRIPT_EXAMPLE = 'script_example'

# Framework fields
_NAME = 'process_name'
_LOG_FILENAME = 'log_filename'
_LOG_TAG = 'log_tag'
_PID_FILENAME = 'pid_filename'
_CLASSNAME = 'classname'
_TIME_QUALIFIER = 'time_qualifier'


def _create_context_entry(process_name,
                          classname,
                          token,
                          time_qualifier,
                          pid_file=None,
                          log_file=None):
    """ forms process context entry """
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
        _TIME_QUALIFIER: time_qualifier
    }


class ProcessContext:
    # process_context format: "process_name": {
    # process_name
    # log_filename
    # log_tag
    # pid_filename
    # full_classname
    # time_qualifier
    # }

    QUALIFIER_REAL_TIME = '_real_time'
    QUALIFIER_BY_SCHEDULE = '_by_schedule'
    QUALIFIER_HOURLY = '_hourly'
    QUALIFIER_DAILY = '_daily'
    QUALIFIER_MONTHLY = '_monthly'
    QUALIFIER_YEARLY = '_yearly'

    logger_pool = dict()

    PROCESS_CONTEXT = {
        PROCESS_SCRIPT_EXAMPLE: _create_context_entry(
            process_name=PROCESS_SCRIPT_EXAMPLE,
            classname='workers.example_script_worker.main',
            token=_TOKEN_SCRIPT_EXAMPLE,
            time_qualifier=QUALIFIER_REAL_TIME),
        PROCESS_CLASS_EXAMPLE: _create_context_entry(
            process_name=PROCESS_CLASS_EXAMPLE,
            classname='workers.abstract_worker.AbstractWorker.start',
            token=_TOKEN_CLASS_EXAMPLE,
            time_qualifier=QUALIFIER_DAILY),

        'TestAggregator': _create_context_entry(
            process_name='TestAggregator',
            classname='',
            token='test',
            time_qualifier=''),
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


if __name__ == '__main__':
    pass