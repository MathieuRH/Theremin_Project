import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import socket

def int_to_bytes(x):
    x = x %256
    x = hex(x)
    if length(x) == 3:
        x = '\x0'+x[-1]
    else: #length == 4
        x = '\x' + x[-2:]

class ThereminSocketServer():
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
                
class LeapListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print ("Initialized")
        self.server = ThereminSocketServer()
        
    def on_connect(self, controller):
        print( "Theremin connected")

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print ("Disconnected")

    def on_exit(self, controller):
        print ("Exited")

    def on_frame(self, controller):
        # initialize byte string
        data = b'\x00\x00'
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        for hand in frame.hands:
            handType = "Left hand" if hand.is_left else "Right hand"
            if handType == "Right hand":
                xmin = -50
                xmax = 150
                ymin = 70
                ymax = 250
    
                x = hand.palm_position.x
                x = min(max(xmin,x),xmax)
                x = (x - xmin) / (xmax-xmin) * 255
                x = int(x)
                x = int_to_bytes(x)
                
                y = hand.palm_position.y
                y = min(max(ymin,y),ymax)
                y = (y - ymin) / (ymax-ymin) * 255
                y = int(y)
                y = int_to_bytes(y)
                
                data = x + y
        print(data)
        self.server.send(data)
        return 0

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    
    # Create a sample listener and controller
    listener = LeapListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print ("Press Enter to quit...")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
