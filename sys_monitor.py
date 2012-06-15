#!/usr/bin/python

from os import sysconf, sysconf_names
from time import sleep

# getconf -v POSIX_V6_LP64_OFF64 CLK_TCK

class SystemMonitor(object):
    def __init__(self, host = None, interval=1):
        self.interval = interval
        self.host = host
        
        if self.host:
            # get data from remote system
            pass
        else:
            # get data from local system
            self.jiffy = sysconf(sysconf_names['SC_CLK_TCK'])
            self.cpu_count = sysconf(sysconf_names['SC_NPROCESSORS_ONLN'])
        
    def cpu_usage(self):
        old_values=[]
        
        while True:
            sleep(self.interval)
            
            cpu_line = open('/proc/stat',  'r').readline()
            new_values = map(int, filter(None, cpu_line.split()[1:]))
            
            if old_values:
                current = map(lambda t1, t2: t1 - t2, new_values, old_values)                    
                yield [ (value * 100 / (self.jiffy * self.interval)) / self.cpu_count for value in current ]        
            
            old_values = new_values
            
    def memory_usage(self):
        pass
        
    def load_average(self):
        pass

if __name__ == '__main__':
    sysmon = SystemMonitor(interval=0.1)
    for cpu in sysmon.cpu_usage():
        print cpu
