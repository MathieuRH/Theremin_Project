'''
# NB : Très long au démarrage, pas possible de faire quelque chose en parallèle --> pire que time.sleep()
import sched, time

s = sched.scheduler(time.time, time.sleep)
def do_something(sc): 
    print("Doing stuff...")
    print(1)
    s.enter(2, 1, do_something, (sc,))

s.enter(60, 1, do_something, (s,))
s.run()
'''

        
'''
#Test fonctionnel de threads
import threading, time

def hello():
    print("hello, world")

WAIT_SECONDS = 5

class foo_training():
    def hello(self):
        print("hello, world")
    
    def foo(self):
        hello()
        self.t_foo = threading.Timer(WAIT_SECONDS, self.foo)
        self.t_foo.start()
    
    def foo_stop(self):
        self.t_foo.cancel()
        # Timer._Thread__stop()
        
a = foo_training()
a.foo()

# t = threading.Timer(30.0, hello)
# t.start()  # after 30 seconds, "hello, world" will be printed

i = 0
while (True):
    print("passage 1")
    time.sleep(1)
    print("passage 2")
    time.sleep(5)
    print("passage 3")
    time.sleep(1)
    a.foo_stop()
    
'''

import threading
import numpy as np
import simpleaudio as sa
import tkinter
import time

can_width=1500
can_height=200
x = 0
y = 0
play = 0
Fe = 44100
WAIT_SECONDS = 0.050 #50 ms entre deux notes jouées

memory_frequency = 0
ref_tremolo = time.time()
tremolo_max = 5

def note(f, vol, trem=0, T = 0.15, wf = 128, br = 128, fe = Fe):
    """"Return the Theremin sound af a note of frequency f, volume vol, for a duration T (default T=0.05s)
    trem stands for tremolo : when you stay in the same spot the note vibrates a little
    Minimum theroretical duration is 0.013ms, but due to start and stop increments we need more"""
    
    t = np.linspace(0,T,np.int(fe*T))
    note = 2048*np.tanh((np.sin(2*np.pi*f*t+np.sin(2*np.pi*trem*t)) + 0.8*wf/255)*6*(0.35))
    note = fade_in(note, 0.05, fe)
    note = fade_out(note, 0.05, fe)
    
    # Ensure that highest value is in 16-bit range
    audio = note * (2**15 - 1) / np.max(np.abs(note)) * vol
    # Convert to 16-bit data
    audio = audio.astype(np.int16)
    return audio

def fade_in (snd, fade_length, fe):
    factor = 0
    step = 1/(fe*fade_length+1)
    for index in range(len(snd)):
        sample = snd[index]
        if index <= fade_length*fe:
            snd[index] = sample*factor
            factor += step
    return snd

def fade_out (snd, fade_length, fe):
    factor = 0
    step = 1/(fe*fade_length+1)
    for index in range(len(snd)-1, -1, -1):
        sample = snd[index]
        if index >= len(snd)-fade_length*fe:
            snd[index] = sample*factor
            factor += step
    return snd

def maj_tremolo(t):
    """Retourne la valeur du trémolo en fonction du temps passé sur la même note
    Pas de trémolo sur les 0.5 premières secondes de la note, après on monte graduellement jusqu'à 1 sec"""
    global tremolo_max
    if t<=0.5:
        return 0
    else :
        return min (tremolo_max*(t-0.5)/0.5, tremolo_max)

class Appel():
    """Fonction qui s'appelle toutes les WAIT_SECONDS pour jouer la note suivante"""
    
    def hello(self):
        print("hello, world")
    
    def commence(self):
        global frequence, memory_frequency, ref_tremolo
        # Condition d'amplification de trémolo : si on garde la même note un petit trémolo s'ajoute
        if frequence != memory_frequency :
            ref_tremolo = time.time()
            
        tremolo = maj_tremolo(time.time()-ref_tremolo)
        audio = note(frequence, volume, tremolo)
        memory_frequency = frequence
        
        sa.play_buffer(audio, 1, 2, Fe)
        self.t = threading.Timer(WAIT_SECONDS, self.commence)
        self.t.start()
    
    def stop(self):
        self.t.cancel()
        # Timer._Thread__stop()
        
musique = Appel()

# t = threading.Timer(30.0, hello)
# t.start()  # after 30 seconds, "hello, world" will be printed
    
#############################
#   Création du canvas      #
#############################

root = tkinter.Tk()
canvas = tkinter.Canvas(root, width = can_width, height = can_height)
canvas.pack()


def motion(event):
    global frequence, volume, can_width, can_height
    #NB : Temps moyen entre deux lancement de fonctions de signal : 13ms
    #t_min = 12ms (très rarement moins)
    x, y = event.x, event.y
    volume = y/(can_height*1.05)
    frequence = x
    print("volume : ", volume)
    print("Frequence : ", frequence)
    
    
def callback(event):
    global play, musique
    play = 1-play
    print("play = ", play)
    if (play==1):
        print("strating musique...")
        musique.commence()
    else :
        print("stopping musique...")
        musique.stop()
        
def stopMusique():
    global musique
    musique.stop()

canvas.bind('<Motion>', motion)
canvas.bind('<Button-1>', callback)
stopButton = tkinter.Button(root, text ="STOP", command = stopMusique)
stopButton.pack()
root.mainloop()
