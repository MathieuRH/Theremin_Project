import threading
import numpy as np
import simpleaudio as sa
import tkinter
import time

can_width = 800
can_height = 200
x = 0
y = 0
play = 0
Fe = 44100
WAIT_SECONDS = 0.070 # ms entre deux notes jouées

memory_frequency = 0
ref_tremolo = time.time()
tremolo_max = 10
tremolo_delay = 0.4

#Paramètres du leap motion
xmin = 0
xmax = 800
ymin = 70
ymax = 250

#Choix des notes minimale et maximale :
# ref_min : numéro de la note minimale
# ref_max : numéro de la note maximale
# NB : La440 = note n°49
# 12 notes par octave (La220 = n°37; La880 = n°61)
ref_min = 37
ref_max = 61

#Calibration de la gamme pouvant être jouée
def freq_numNote(n):
    return 2**((n-49)/12)*440

nb_notes = ref_max-ref_min+1
table_abscisses = np.linspace(xmin, xmax, nb_notes)
table_frequences = []
for i in range(nb_notes):
    table_frequences.append(freq_numNote(ref_min+i))



def note(f, vol, trem=0, T = 0.2, wf = 128, br = 128, fe = Fe):
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
    global tremolo_max, tremolo_delay
    if t<=tremolo_delay:
        return 0
    else :
        return min (tremolo_max*(t-tremolo_delay)/tremolo_delay, tremolo_max)

def calcul_frequence(pos):
    """
    Fonction de calcul de la fréquence jouée en fonction de la position de la main et de la calibration initiale.
    
    Parameters
    ----------
    pos : Position de l'abscisse de la main

    Returns
    -------
    Fréquence de jeu calculée

    """
    global xmin, xmax, table_abscisses, table_frequences
    
    #On cherche dans quel intervalle se situe la note que l'on joue
    indice_intervalle = 0
    while(table_abscisses[indice_intervalle+1]<pos):
        indice_intervalle += 1
        
    print(indice_intervalle)
    #On retrouve la fréquence en interpolant à partir des deux notes connues les plus proches
    pourcentage_pos = (pos-table_abscisses[indice_intervalle])/(table_abscisses[indice_intervalle+1]-table_abscisses[indice_intervalle])
    pente_freq = table_frequences[indice_intervalle+1]-table_frequences[indice_intervalle]
    f = table_frequences[indice_intervalle]+pourcentage_pos*pente_freq
    
    return f

class Appel():
    """Fonction qui s'appelle toutes les WAIT_SECONDS pour jouer la note suivante"""
    
    def hello(self):
        print("hello, world")
    
    def commence(self):
        global frequence, volume, memory_frequency, ref_tremolo
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
    global musique, play
    print("Stopping music...")
    musique.stop()
    play = 0
    
#############################
#   Création du canvas      #
#############################

root = tkinter.Tk()
stopButton = tkinter.Button(root, text ="STOP", command = stopMusique)
stopButton.pack()
canvas = tkinter.Canvas(root, width = can_width, height = can_height)
canvas.pack()

def motion(event):
    global frequence, volume, can_width, can_height
    #NB : Temps moyen entre deux lancement de fonctions de signal : 13ms
    #t_min = 12ms (très rarement moins)
    x, y = event.x, event.y
    volume = y/(can_height*1.05)
    frequence = calcul_frequence(x)
    print("volume : ", volume)
    print("Coordonnée : ", x)
    print("Frequence : ", frequence)

canvas.bind('<Motion>', motion)
canvas.bind('<Button-1>', callback)
root.mainloop()
