#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from multiprocessing import Process

class ManagedProcess(object):
    """
    This class starts a new Process and checks the availability
    of that process. If the process dies, it will be restarted.
    """

    def __init__(self, proc, *args, **kwargs):
        self.proc = proc
        self.args = args
        self.kwargs = kwargs
        self.stop = False

    def start(self):
        while not self.stop:
            self.child = Process(target=self.proc, args=self.args, kwargs=self.kwargs)
            self.child.daemon = True
            print "[+] starting..."
            self.child.start()
            while not self.stop:
                self.child.join(0.1)
                if not self.child.is_alive():
                    print "[+] child died, restarting..."
                    break

    def stop(self):
        self.stop = True

if __name__ == '__main__':
    def sleep(secs):
        import time
        time.sleep(secs)

    mp = ManagedProcess(sleep, 10000)
    mp.start()
