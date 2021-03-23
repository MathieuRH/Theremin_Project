import simpleaudio as sap
import numpy as np
import socket
from time import sleep
import sys
import threading 

class ThereminSocketClient():
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
            print('Received', repr(self.data))
        else:
            print('socket not opened (yet?)')

class ThereminPlayer():
    def __init__(self):
        self.client  = ThereminSocketClient()
        self.fs = 44100
        self.start()
        
    def play(self,frequency, seconds):
        # Generate array with seconds*sample_rate steps, ranging between 0 and seconds
        t = np.linspace(0, seconds, int(seconds * self.fs), False)

        # Generate a 440 Hz sine wave
        note = np.sin(frequency * t * 2 * np.pi)

        # Ensure that highest value is in 16-bit range
        audio = note * (2**15 - 1) / np.max(np.abs(note))
        audio /= 5;
        # Convert to 16-bit data
        audio = audio.astype(np.int16)

        # Start playback
        play_obj = sap.play_buffer(audio, 1, 2, self.fs)
        # Wait for playback to finish before exiting
        # play_obj.wait_done()
        
    def start(self):
        self.client.receive()
        data = self.client.data[-2:]
        if b'1' not in self.client.data:
            self.play(300,0.1)
        else:
            self.play(500,0.1)
        threading.Timer(0.05, self.start()).start()
        
def main():
    player = ThereminPlayer()

if __name__ == "__main__":
    main()
