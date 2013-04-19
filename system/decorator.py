"""
Created on 2012-04-24

@author: Bohdan Mushkevych
"""
import functools


def thread_safe(method):
    """ wraps function with lock acquire/release cycle """

    @functools.wraps(method)
    def _locker(self, *args, **kwargs):
        try:
            self.lock.acquire()
            return method(self, *args, **kwargs)
        finally:
            self.lock.release()
    return _locker
