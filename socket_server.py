#!/usr/bin/python

import socket
from threading import Thread
from select import select

class TCPServerChild(Thread):
    """
    TCPServerChild: class for use with TCPServer. Uses the Thread subclass.
    
    @socket: client tuple in the form of (socket, client_addr)
    @run: this function should be overwritten with client-handling code
    """
    
    def __init__(self, socket):
        Thread.__init__(self)
        
        self.socket, self.address = socket
        
    def read(self, bytes=1024, timeout=None):
        if timeout:
            readable, writable, errored = select([self.socket, ], [], [], timeout)
            if self.sock in readable:
                return self.socket.recv(bytes)
            else:
                return None
        else:
            return self.socket.recv(bytes)
        
    def run(self):
        """ overwrite with initial server function """
        
        self.socket.close()

class TCPEchoServer(TCPServerChild):
    """ Threaded server example """
    
    def run(self):
        data = self.read()
        self.socket.send(data)
        self.socket.close()

class TCPServer(object):
    """
    TCPServer class: creates a listening socket and spawns threads for every connected client
    
    @bind_socket: socket tuple in the form (ipaddr, socket) to bind to
    @callback: class with subclass of TCPServerChild to handle each client connection
    @max_connections: maximum number of concurrend client connections
    """
    
    thread_pool = []
    
    def __init__(self, bind_socket, callback, max_connections = 10):  
        self.bind_socket = bind_socket
        self.max_connections = max_connections
        self.callback = callback
    
    def serve_forever(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.bind_socket)
        self.sock.listen(self.max_connections)
        
        while True:
            readable, writable, errored = select([self.sock, ], [], [], 1)
            if self.sock in readable:
                self.thread_pool.append(self.callback(self.sock.accept()))
                self.thread_pool[-1].start()
            
            # clean up
            for thread in self.thread_pool[:]:
                if not thread.is_alive():
                    self.thread_pool.remove(thread)
    
            print len(self.thread_pool)
            
if __name__ == '__main__':
    server = TCPServer(('127.0.0.1', 6666), TCPEchoServer)
    server.serve_forever()
