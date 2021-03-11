import threading 
from socketclient import SocketClient
from soundgenerator import SoundGenerator
    
class ThereminPlayer():
    def __init__(self):
        self.i = 0
        #initialize socket client
        self.client  = SocketClient()
        #initialize sound generator
        self.music = SoundGenerator()
        
        #start main callback
        #it handles both the socket client and the sound generation
        self.WAIT_SECONDS = 0.050 #time between two notes
        self.start()
      
    def callback(self):
        self.i += 1
        print("frame "+str(self.i))
        #get data from client
        self.client.receive()
        #extract values
        data = self.client.data[-20:]
        self.music.on = True if int(data[0:4], 16) else False
        xLeft = int(data[4:8], 16)
        yLeft = int(data[8:12], 16)
        xRight = int(data[12:16], 16)
        yRight = int(data[16:20], 16)
        #change value range from 0-255 to coherent values for volume and frequency
        self.music.frequency = self.music.first_note * 2**(xRight*(self.music.number_of_notes-1)/12/255)
        self.music.volume = yLeft / 255
        print("sound "+str(self.music.on) +"\nfrequency "+str(self.music.frequency) +"\nvolume "+str(self.music.volume)+"\ntremolo "+str(self.music.tremolo)+"\n\n")
        
        #play sound
        self.music.play()
        
    def start(self):
        #if not self.clavier.terminate:
        #call callback once
        self.callback()
        #set timer for next call
        self.thread = threading.Timer(self.WAIT_SECONDS, self.start)
        #start timer
        self.thread.start()
        

def main():
    player = ThereminPlayer()

if __name__ == "__main__":
    main()