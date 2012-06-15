#!/usr/bin/python

from threading import Thread
from Queue import Queue, Empty

class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    
    func = None
    args = None
    kargs = None
    
    def __init__(self, tasks, results):
        Thread.__init__(self)
        
        self.tasks = tasks
        self.results = results
        
        self.daemon = True
        self.start()
    
    def run(self):
        while True:
            try:
                self.func, self.args, self.kargs = self.tasks.get(False)
            except Empty:
                pass
            
            if self.func:
                try: self.results.put(self.func(*self.args, **self.kargs))
                except Exception, e: print e

class ThreadPool(object):
    """Pool of threads consuming tasks from a queue"""
    
    def __init__(self, num_threads):
        self.tasks = Queue()
        self.results = Queue()
        self.num_threads = num_threads
        
        for _ in range(self.num_threads): Worker(self.tasks, self.results)

    def workload(self, func, *args, **kargs):
        """ set current workload for threadpool """
        
        for _ in range(self.num_threads): self.tasks.put((func, args, kargs))

    def query(self):
        """ get return values from worker threads """
        
        while True:
            yield self.results.get()
            self.results.task_done()

def get_time():
    from time import time, sleep
    sleep(1)
    return time()

if __name__ == '__main__':
    pool = ThreadPool(10)
    pool.workload(get_time)
    for result in pool.query():        
        print result
    
    
