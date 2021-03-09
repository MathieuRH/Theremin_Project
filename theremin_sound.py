#Synthese du son du Theremin
import numpy as np
import simpleaudio as sa
import time

ref = time.time()

#############################
#Exemple de creation de note#
#############################
frequency = 505  # exemple note if needed
volume = 0.1
Fe = 44100

freq_gamme_essai = [385, 423, 482, 505, 574, 651, 728, 770]
#wf = Waveform (0~pure sine ; 256~pipeau)
#br = Brightness (0~un peu sourd ; 256~clear af)
#vol = volume percentage (0-1)
#f = note frequency
def noteTH(f, vol, T = 1, wf = 128, br = 128, trem=2, fe = Fe):
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


def note(f, vol, T = 1, ft = 5, fe = Fe):
    """"Return the Theremin sound from the spectrogram analysis"""
    #ft = frequence tremolo
    
    amplitudes = [1249, 194.6, 20.22, 19.49, 23.2] #Pour f = 285 Hz
    t = np.linspace(0,T,np.int(fe*T))
    bases = [np.sin(2*np.pi*i*f*t) for i in range(len(amplitudes))]
    note_amp = [amplitudes[i]*bases[i] for i in range(len(amplitudes))]
    note = sum(note_amp)
    
    note = fade_in(note, 0.05, fe)
    note = fade_out(note, 0.05, fe)
    
    # Ensure that highest value is in 16-bit range
    audio = note * (2**15 - 1) / np.max(np.abs(note)) * vol
    # Convert to 16-bit data
    audio = audio.astype(np.int16)
    return audio

i = 0
while i<len(freq_gamme_essai):
    audio = noteTH(freq_gamme_essai[i], volume)
    play = sa.play_buffer(audio, 1, 2, Fe)
    play.wait_done()
    i += 1





