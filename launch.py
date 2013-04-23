#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shutil
import sys
import subprocess
import virtualenv

from optparse import OptionParser
from os import path


PROCESS_STARTER = 'process_starter.py'
PROJECT_ROOT = path.abspath(path.dirname(__file__))

VE_SCRIPT = path.join(PROJECT_ROOT, 'scripts', 'install_virtualenv')
VE_ROOT = path.join(PROJECT_ROOT, '.ve')

def init_parser():
    """Setup our command line options"""
    parser = OptionParser()
    parser.add_option("-a", "--app", action="store",  help="application to start (process name)")
    parser.add_option("-n", "--interactive", action="store_true", help="run in interactive (non-daemon) mode")
    parser.add_option("-m", "--main", action="store_true", help="Python script with main function to start")
    parser.add_option("-r", "--run", action="store_true", help="start process supervisor for this box")
    parser.add_option("-k", "--kill", action="store_true", help="kill process supervisor for this box")
    parser.add_option("-q", "--query", action="store_true", help="query application's state")
    parser.add_option("-i", "--install_ve", action="store_true", help="install a virtualenv for the runtime to use")
    parser.add_option("-s", "--shell", action="store_true", help="run an ipython shell within the virtualenv")
    parser.add_option("-t", "--tests", action="store_true", help="run tests")
    parser.add_option("-x", "--xunit", action="store_true", help="run tests with coverage and xunit output for hudson")
    parser.add_option("-l", "--lint", action="store_true", help="run pylint on project")
    parser.add_option("-o", "--outfile", action="store", help="save results from a report to a file")
    return parser


def get_python():
    """Determine the path to the virtualenv python"""
    if sys.platform == 'win32':
        python = path.join(VE_ROOT, 'Scripts', 'python.exe')
    else:
        python = path.join(VE_ROOT, 'bin', 'python')
    return python


def go_to_ve():
    """Rerun this script within the virtualenv with same args"""
    if not path.abspath(sys.prefix) == VE_ROOT:
        python = get_python()
        retcode = subprocess.call([python, __file__] + sys.argv[1:])
        sys.exit(retcode)


def install_environment(root):
    """Install our virtual environment; removing the old one if it exists"""
    print 'Installing virtualenv into %s' % root
    if path.exists(root):
        shutil.rmtree(root)
    virtualenv.logger = virtualenv.Logger(consumers=[])
    virtualenv.create_environment(root, site_packages=False)
    retcode = subprocess.call([VE_SCRIPT, PROJECT_ROOT, root])
    sys.exit(retcode)


def install_or_switch_to_virtualenv(options):
    """Installs, switches, or bails"""
    if options.install_ve:
        install_environment(VE_ROOT)
    elif path.exists(VE_ROOT):
        go_to_ve()
    else:
        sys.stdout.write('No virtualenv detected, please run ./launch.py --install_ve \n')
        sys.exit(1)


def dispatch_options(parser, options, args):
    if options.run:
        daemonize = True if options.interactive else False
        start_process(options, daemonize)
    elif options.main:
        start_script(options)
    elif options.kill:
        stop_process(options)
    elif options.query:
        query_configuration(options)
    elif options.shell:
        run_shell(options)
    elif options.lint:
        run_lint(options)
    elif options.tests:
        run_tests(options)
    elif options.xunit:
        run_xunit(options)
    else:
        parser.print_help()


def valid_process_name(function):
    """ Decorator validates if the --app parameter is registered in the process_context
        :raise #ValueError otherwise """
    from system.process_context import ProcessContext

    def _wrapper(options, *args, **kwargs):
        if options.app not in ProcessContext.PROCESS_CONTEXT:
            msg = 'Aborting: application <%r> defined by --app option is unknown. \n' % options.app
            sys.stdout.write(msg)
            raise ValueError(msg)
        return function(options, *args, **kwargs)
    return _wrapper


@valid_process_name
def query_configuration(options):
    """ Queries process state """
    from system import process_helper
    process_helper.poll_process(options.app)


@valid_process_name
def start_script(options):
    """Start up process in interactive mode as a fabric script """
    from system.process_context import ProcessContext
    try:
        sys.stdout.write('INFO: Starting %s \n' % ProcessContext.get_classname(options.app))
        parts = ProcessContext.get_classname(options.app).split('.')
        module = ".".join(parts[:-1])
        m = __import__( module )
        # load module holding main function
        m = getattr(m, parts[-2])
        m.main(args)
    except Exception as e:
        sys.stderr.write('Exception on starting %s : %s \n' % (options.app, str(e)))


@valid_process_name
def start_process(options, daemonize):
    """Start up specific daemon """
    import psutil
    from system import process_helper

    try:
        pid = process_helper.get_process_pid(options.app)
        if pid is not None:
            if psutil.pid_exists(pid):
                message = 'ERROR: Process %r is already running with pid %r\n' % (options.app, pid)
                sys.stderr.write(message)
                sys.exit(1)

        process_helper.start_process(options.app)
    except Exception as e:
        sys.stderr.write('Exception on starting %s : %s \n' % (options.app, str(e)))


@valid_process_name
def stop_process(options):
    """Stop specific daemon"""
    from system import process_helper

    try:
        pid = process_helper.get_process_pid(options.app)
        if pid is None or process_helper.poll_process(options.app) == False:
            message = 'ERROR: Process %r is already terminated %r\n' % (options.app, pid)
            sys.stderr.write(message)
            sys.exit(1)

        process_helper.kill_process(options.app)
    except Exception as e:
        sys.stderr.write('Exception on killing %s : %s \n' % (options.app, str(e)))


def run_shell(options):
    """Run IPython in the virtualenv"""
    import IPython
    # Stolen from django
    # Explicitly pass an empty list as arguments, because otherwise IPython
    # would use sys.argv from this script.
    shell = IPython.Shell.IPShell(argv=[])
    shell.mainloop()


def run_lint(options):
    from pylint import lint
    from pylint.reporters.text import ParseableTextReporter
    from settings import testable_modules as modules

    if options.outfile:
        output = open(options.outfile, 'w')
    else:
        output = sys.stdout

    config = "--rcfile=" + path.join(PROJECT_ROOT, 'pylint.rc')
    lint.Run([config] + modules,
        reporter=ParseableTextReporter(output=output), exit=False)


def load_all_tests():
    import unittest
    from settings import test_cases

    return unittest.defaultTestLoader.loadTestsFromNames(test_cases)


def run_tests(options):
    import unittest
    import logging
    import settings

    settings.enable_test_mode()

    argv = [sys.argv[0]] + args
    try:
        unittest.main(module=None, defaultTest='__main__.load_all_tests',
            argv=argv)
    except SystemExit, e:
        if e.code == 0:
            logging.info('PASS')
        else:
            logging.error('FAIL')
            raise


def run_xunit(options):
    import unittest
    import xmlrunner
    import settings

    settings.enable_test_mode()

    output = 'reports'
    if options.outfile:
        output = options.outfile

    argv = [sys.argv[0]] + args
    try:
        unittest.main(
            module=None,
            defaultTest='__main__.load_all_tests',
            argv=argv,
            testRunner=xmlrunner.XMLTestRunner(output=output))
    except SystemExit:
        pass


# Ensure we are running in a virtual environment
if __name__ == "__main__":
    parser = init_parser()
    (options, args) = parser.parse_args()
    install_or_switch_to_virtualenv(options)
    dispatch_options(parser, options, args)
