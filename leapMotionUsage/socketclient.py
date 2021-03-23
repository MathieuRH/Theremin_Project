import sys, socket

class SocketClient():
    def __init__(self):
        self.HOST = '127.0.0.1' # localhost
        self.PORT = 50009 # has to be the equal to the server port
        self.running = False
        self.s = None
        for res in socket.getaddrinfo(self.HOST, self.PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                self.s = socket.socket(af, socktype, proto)
            except OSError as msg:
                self.s = None
                continue
            try:
                self.s.connect(sa)
            except OSError as msg:
                self.s.close()
                self.s = None
                continue
            break
        if self.s is None:
            print('could not open socket')
            sys.exit(1)
        else:
            self.running = True
    def receive(self):
        if self.running:
            self.data = self.s.recv(1024)
            print('Received', self.data)
        else:
            print('socket not opened (yet?)')