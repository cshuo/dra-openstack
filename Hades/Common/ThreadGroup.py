__author__ = 'pike'

import eventlet

def _thread_done(gt, *args, **kwargs):
    """Callback function to be passed to GreenThread.link() when we spawn()
    Calls the :class:`ThreadGroup` to notify if.

    """
    kwargs['group'].thread_done(kwargs['thread'])

class Thread(object):
    """Wrapper around a greenthread, that holds a reference to the
    :class:`ThreadGroup`. The Thread will notify the :class:`ThreadGroup` when
    it has done so it can be removed from the threads list.
    """

    def __init__(self, thread, group):
        self.thread = thread
        self.thread.link(_thread_done, group = group, thread = self)

    def stop(self):
        self.thread.kill()

    def wait(self):
        return self.thread.wait()()

    def link(self, func, *args, **kwargs):
        self.thread.link(func, *args, **kwargs)

class ThreadGroup(object):
    """The point of the ThreadGroup class is to:

    * keep track of timers and greenthreads (making it easier to stop them
      when need be).
    * provide an easy API to add timers.
    """
    def __int__(self, thread_pool_size = 10):
        self.pool = eventlet.greenpool.GreenPool(thread_pool_size)
        self.threads = []
        self.timers = []

    def add_thread(self, callback, *args, **kwargs):
        gt = self.pool.spawn(callback, *args, **kwargs)
        th = Thread(gt, self)
        self.threads.append(th)
        return th

    def thread_done(self, thread):
        self.threads.remove(thread)

