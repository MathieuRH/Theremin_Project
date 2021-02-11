import threading 
from socketclient import SocketClient
from keyboardhandler import KeyboardHandler
from soundgenerator import SoundGenerator
    
class ThereminPlayer():
    def __init__(self):
        self.i = 0
        #initialize socket client
        self.client  = SocketClient()
        #initialize keyboard listener
        self.clavier = KeyboardHandler()
        #initialize sound generator
        self.music = SoundGenerator()
        
        #start main callback
        #it handles both the socket client and the sound generation
        self.WAIT_SECONDS = 0.050 #time between two notes
        self.start()
        #start keyboard callback
        self.clavier.start()
      
    def callback(self):
        self.i += 1
        print("frame "+str(self.i))
        #get data from client
        self.client.receive()
        #extract values
        data = self.client.data[-16:]
        xLeft = int(data[:4], 16)
        yLeft = int(data[4:8], 16)
        xRight = int(data[8:12], 16)
        yRight = int(data[12:16], 16)
        #change value range from 0-255 to coherent values for volume and frequency
        self.music.frequency = xRight + 200
        self.music.volume = yRight / 255
        print("f "+str(self.music.frequency) +"\nv "+str(self.music.volume)+"\ntrem "+str(self.music.tremolo)+"\n\n")
        
        #link sound generator to keyboard spacebar
        self.music.on = self.clavier.toggle
        #play sound
        self.music.play()
        
    def start(self):
        if not self.clavier.terminate:
            #call callback once
            self.callback()
            #set timer for next call
            self.thread = threading.Timer(self.WAIT_SECONDS, self.start)
            #start timer
            self.thread.start()
        else:
            self.terminate()
            
    def stop(self):
        self.thread.cancel()
            
    def terminate(self):
        #stop main callback
        self.stop()
        #stop keyboard callback
        self.clavier.stop()

def main():
    player = ThereminPlayer()

if __name__ == "__main__":
    main()