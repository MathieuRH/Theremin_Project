import simpleaudio as sa
import numpy as np
from time import time

class SoundGenerator():
    def __init__(self):
        #sound synthesis paramters
        self.fe = 44100
        self.first_note = 220 #lowest note in Hz
        self.number_of_notes = 25 
        #individual notes parameters
        self.tremolo_max = 5
        self.tremolo_start = 0.5
        self.tremolo_end = 1
        self.quarter_step = 2**(1/24)
        self.t_in = 0.05
        self.t_out = 0.05
        
        #initialize internal variables
        self.frequency = self.first_note
        self.volume = 0.05
        self.memory_frequency = 0
        self.ref_tremolo = time()
        self.tremolo = 0
        self.on = False
        
    def note(self, f, vol, trem=0, T = 0.15, wf = 128, br = 128):
        """"Return the Theremin sound af a note of frequency f, volume vol, for a duration T (default T=0.05s)
        trem stands for tremolo : when you stay in the same spot the note vibrates a little
        Minimum theroretical duration is 0.013ms, but due to start and stop increments we need more"""
        
        t = np.linspace(0,T,np.int(self.fe*T))
        # main theremin waveform with tremolo included
        audio = np.tanh((np.sin(2*np.pi*f*t+np.sin(2*np.pi*trem*t)) + 0.8*wf/255)*6*(0.35))
        # apply fade in and out
        audio = self.fade_in(audio)
        audio = self.fade_out(audio)
        # normalize sound
        audio /= np.max(np.abs(audio))
        # Ensure that highest value is in 16-bit range
        audio *=  (2**15 - 1) 
        #apply volume 
        audio *= vol
        # Convert to 16-bit data
        audio = audio.astype(np.int16)
        return audio

    def fade_in (self, snd):
        factor = 0
        step = 1/(self.fe*self.t_in+1)
        for index in range(len(snd)):
            if index <= self.t_in*self.fe:
                snd[index] *= factor
                factor += step
        return snd

    def fade_out (self, snd):
        factor = 0
        step = 1/(self.fe*self.t_out+1)
        for index in range(len(snd)-1, -1, -1):
            if index >= len(snd)-self.t_out * self.fe:
                snd[index] *= factor
                factor += step
        return snd

    def maj_tremolo(self):
        """Retourne la valeur du trémolo en fonction du temps passé sur la même note
        Pas de trémolo sur les tremolo_start premières secondes de la note, après on monte graduellement jusqu'à tremolo_end sec
        avec une interpolation linéare"""
        #check if frequency is less than a quarter step away from previous note 
        if (self.frequency < self.memory_frequency/self.quarter_step) or (self.frequency > self.memory_frequency*self.quarter_step):
            self.ref_tremolo = time()
            self.memory_frequency = self.frequency
            self.tremolo = 0
        else:
            # get tremolo value
            t = time()-self.ref_tremolo
            if t <= self.tremolo_start:
                self.tremolo = 0
            elif t<= self.tremolo_end:
                self.tremolo = self.tremolo_max*(t-self.tremolo_start)/(self.tremolo_end-self.tremolo_start)
            else :
                self.tremolo = self.tremolo_max
        
    def play(self):
        # Condition d'amplification de trémolo : si on garde la même note un petit trémolo s'ajoute
        self.maj_tremolo()
        #play note
        if self.on:
            audio = self.note(self.frequency, self.volume, self.tremolo)
            sa.play_buffer(audio, 1, 2, self.fe)
