# Theremin project
This python project uses python and a leap motion to simulate a theremin. 
As the latest version of the Leap motion API does not support Python, we use an older version.
This versoin only work with Python2.
Thus we use Python2 to interact with the Leap Motion and Python3 for the rest od the code (mainly to use simpleaudio)
# Files
The project contains the following files :
## socketserver.py
In python2, define a SocketServer class.
## leapcontroller.py
In python2, define a LeapListener class and a main to connect to the leap motion and send data to a socket server.
## socketclient.py
In python3, define a SocketSlient class.
## keyboardcontroller.py
In python3, define a KeyboardController class. Spacebar activates and deactivates sound. Escape close all the scripts.
## soundgenerator.py
In python3, define a SoundGenerator class to play sound with simpleaudio.
## thereminplayer.py 
In python3, define a ThereminPlayer class and a main to get socket data, start keyboard callback and play sound.
# Running the project
To run the project, have the correct version of Leap Motion Control Panel installed (see google drive for installation tutorial).
Then launch leapcontroller.py with python2 and thereminplayer.py with python3 (in that order).
Spacebar mute and unmute sound.
Escape terminates the two scripts.
The x coordinate of the right hand control the frequency and its y coordinate controls the volume.