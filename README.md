# Theremin project
This python project uses python and a leap motion to simulate a theremin.
# First part - tkinterUsage
This branch contains the first part of our project, where we worked on two separate applications.
## Simulating a theremin sound - Leap Motion introduction
The files interface_synthesis.py and theremin_sound.py, writtten in python3, will allow you to simulate a theremin controlled by your computer mouse.
The files theremin.py (python2) and audio.py (python3) will allow you to connect a python2 script to the leap motion and to connect a python2 script with a python3 script using a socket connection.

# Second part - leapMotionUsage - Interfacing python2, python3 and the leap motion
This python project uses python and a leap motion to simulate a theremin. 
As the latest version of the Leap motion API does not support Python, we use an older version.
This version only work with Python2.
Thus we use Python2 to interact with the Leap Motion and Python3 for the rest od the code (mainly to use simpleaudio)
## Files
The project contains the following files :
## socketserver.py
In python2, define a SocketServer class.
## leapcontroller.py
In python2, define a LeapListener class and a main to connect to the leap motion and send data to a socket server.
## socketclient.py
In python3, define a SocketSlient class.
## soundgenerator.py
In python3, define a SoundGenerator class to play sound with simpleaudio.
## thereminplayer.py 
In python3, define a ThereminPlayer class and a main to get socket data and play sound.
# Running the project
To run the project, have the correct version of Leap Motion Control Panel installed (see google drive for installation tutorial).
Then launch leapcontroller.py with python2 and thereminplayer.py with python3.
To mute sound, draw a circle counter clockwise. The project start muted.
To unmute sound, draw a circle clockwise with any of your fingers.
The x coordinate of the right hand control the frequency.
The lowest note is above the leap motion, higher notes are played by moving the hand to the right 
The y coordinate of the left hand controls the volume.
You should have your left hand left of the leap motion to leave enough space for your right hand.
