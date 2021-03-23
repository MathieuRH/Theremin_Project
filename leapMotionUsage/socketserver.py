import sys, socket

class SocketServer():
    def __init__(self):
        HOST = '127.0.0.1' # localhost
        PORT = 50009 # arbitrary non-privileged port
        s = None
        for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                                      socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
            af, socktype, proto, canonname, sa = res
            try:
                s = socket.socket(af, socktype, proto)
            except OSError as msg:
                s = None
                continue
            try:
                s.bind(sa)
                s.listen(1)
            except OSError as msg:
                s.close()
                s = None
                continue
            print("Socket server connected")
            break
        if s is None:
            print('could not open socket')
            sys.exit(1)
        self.conn, addr = s.accept()
        if self.conn:
            print('Connected by', addr)
    def send(self,data):
        self.conn.send(data)
        print("sending " + data)