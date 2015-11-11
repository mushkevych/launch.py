__author__ = 'Bohdan Mushkevych'

from system.process_context import ProcessContext, _create_context_entry

# User fields
PROCESS_CLASS_EXAMPLE = 'ClassExample'
PROCESS_SCRIPT_EXAMPLE = 'ScriptExample'

# process provides <process context> to unit testing: such as logger, queue, etc
PROCESS_UNIT_TEST = 'UnitTest'

TOKEN_CLASS_EXAMPLE = 'class_example'
TOKEN_SCRIPT_EXAMPLE = 'script_example'


def register_unit_test_context():
    """ Function should be called by #setting.enable_test_mode to register UT classes and functionality """
    ProcessContext.CONTEXT[PROCESS_SCRIPT_EXAMPLE] = _create_context_entry(
        process_name=PROCESS_SCRIPT_EXAMPLE,
        classname='workers.example_script_worker.main',
        token=TOKEN_SCRIPT_EXAMPLE)

    ProcessContext.CONTEXT[PROCESS_CLASS_EXAMPLE] = _create_context_entry(
        process_name=PROCESS_CLASS_EXAMPLE,
        classname='workers.abstract_worker.AbstractWorker.start',
        token=TOKEN_CLASS_EXAMPLE)

    ProcessContext.CONTEXT[PROCESS_UNIT_TEST] = _create_context_entry(
        process_name=PROCESS_UNIT_TEST,
        classname='',
        token='unit_test')
