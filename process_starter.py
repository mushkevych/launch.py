"""
Created on 2011-06-15

@author: Bohdan Mushkevych
"""

import sys

from system.process_context import ProcessContext


def get_class(kls):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


def start_by_class(process_name):
    """
    Function creates an instance of a class and calls <code>start</code> method with NO parameters
    """
    sys.stdout.write('INFO: Starting class\' %r start method \n' % ProcessContext.get_classname(process_name))
    klass = get_class(ProcessContext.get_classname(process_name))
    instance = klass(process_name)
    instance.start()


def start_by_function(process_name, *args):
    """
    Function creates an instance of a module and calls <code>main(*args)</code> method on it
    """
    sys.stdout.write('INFO: Starting module\'s %r main function with parameters %r \n'
                     % (ProcessContext.get_classname(process_name), args))
    klass = get_class(ProcessContext.get_classname(process_name))
    instance = klass(process_name)
    instance.main(args)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write('ERROR: no Process Name specified to start \n')
    elif len(sys.argv) == 2:
        process_name = sys.argv[1]
        start_by_class(process_name)
    else:
        process_name = sys.argv[1]
        args = sys.argv[2:]
        start_by_function(process_name, args)