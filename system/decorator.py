__author__ = 'Bohdan Mushkevych'

import sys
import functools
import traceback


def thread_safe(method):
    """ wraps method with lock acquire/release cycle
     decorator requires class instance to have field self.lock of type threading.Lock or threading.RLock """

    @functools.wraps(method)
    def _locker(self, *args, **kwargs):
        assert hasattr(self, 'lock'), \
            'thread_safe decorator applied to method {0}.{1}: missing required field {0}.lock'.\
            format(self.__class__.__name__, method.__name__)

        try:
            self.lock.acquire()
            return method(self, *args, **kwargs)
        finally:
            try:
                self.lock.release()
            except:
                sys.stderr.write('Exception on releasing lock at method {0}'.format(method.__name__))
                traceback.print_exc(file=sys.stderr)

    return _locker
