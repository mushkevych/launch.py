"""
Created on 2011-06-15

@author: Bohdan Mushkevych
"""
from subprocess import PIPE, STDOUT
import sys

import psutil
from psutil import TimeoutExpired
from launch import get_python, PROJECT_ROOT, PROCESS_STARTER
from system.process_context import ProcessContext
from settings import settings


def get_process_pid(process_name):
    """ check for process' pid file and returns pid from there """
    try:
        pid_filename = ProcessContext.get_pid_filename(process_name)
        pf = file(pid_filename, 'r')
        pid = int(pf.read().strip())
        pf.close()
    except IOError:
        pid = None
    return pid


def kill_process(process_name):
    """ method is called to kill a running process """
    try:
        sys.stdout.write('killing: %s {' % process_name)
        pid = get_process_pid(process_name)
        if pid is not None and psutil.pid_exists(int(pid)):
            p = psutil.Process(pid)
            p.kill()
            p.wait()
            ProcessContext.remove_pid_file(process_name)
    except Exception:
        sys.stderr.write('Exception on killing: %s' % process_name, exc_info=True)
    finally:
        sys.stdout.write('}')


def start_process(process_name):
    try:
        sys.stdout.write('start: %s {' % process_name)
        p = psutil.Popen([get_python(), PROJECT_ROOT + '/' + PROCESS_STARTER, process_name],
            close_fds=True,
            cwd=settings['process_cwd'],
            stdin=PIPE,
            stdout=PIPE,
            stderr=STDOUT)
        sys.stdout.write('Started %s with pid = %r' % (process_name, p.pid))
    except Exception:
        sys.stderr.write('Exception on starting: %s' % process_name, exc_info=True)
    finally:
        sys.stdout.write('}')


def poll_process(process_name):
    """ between killing a process and its actual termination lies poorly documented requirement -
        <purging process' io pipes and reading exit status>.
        this can be done either by os.wait() or process.wait()
        :return True if the process is alive and OK and False is the process was terminated """
    try:
        pid = get_process_pid(process_name)
        p = psutil.Process(pid)

        return_code = p.wait(timeout=0.01)
        if return_code is None:
            # process is already terminated
            sys.stdout.write('Process %s is terminated' % process_name)
            return False
        else:
            # process is terminated; possibly by OS
            sys.stdout.write('Process %s got terminated' % process_name)
            return False
    except TimeoutExpired:
        sys.stdout.write('Process %s is alive and OK' % process_name)
        return True
