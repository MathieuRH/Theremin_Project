import sys, Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from socketserver import SocketServer

def int_to_hex(a):
    #ensure integer is between 0 and 255
    a = a %256
    a = hex(a)
    #convert from 0x2 to 0x02
    if len(a) == 3:
        a = a[:2]+"0"+a[2:]
    return a
                
class LeapListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        #iniialize socket server
        self.server = SocketServer()
        print ("Initialized")
        
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
        data = "0x000x000x000x00"
        # Get the most recent frame  information
        frame = controller.frame()
        #gross calibration
        xmin = -50
        xmax = 150
        ymin = 70
        ymax = 250
        for hand in frame.hands:
            handType = "Left hand" if hand.is_left else "Right hand"
            
            #code data between 0 and 255 according to calibration
            x = hand.palm_position.x
            x = min(max(xmin,x),xmax)
            x = (x - xmin) / (xmax-xmin) * 255
            x = int(x)
            x = int_to_hex(x)
            
            y = hand.palm_position.y
            y = min(max(ymin,y),ymax)
            y = (y - ymin) / (ymax-ymin) * 255
            y = int(y)
            y = int_to_hex(y)
            
            # fill data byte string
            if handType == "Right hand":
                data = data[0:8] + x + y
            else:
                data = x + y + data[8:16]
                
        #send data with socket server
        self.server.send(data)

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
    
    # Create a listener and controller
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