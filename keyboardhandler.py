from pynput.keyboard import Listener, Key        
                
class KeyboardHandler():
    def on_press(self, key):
        if key == Key.space:
            print("oh no")
            self.toggle = not self.toggle
        if key == Key.escape:
            print("rip")
            self.terminate = True
    def on_release(self, key):
        pass
    def __init__(self):
        self.toggle = False
        self.terminate = False
        #create keyboard callback
        self.keyboard_callback = Listener(on_press=self.on_press, on_release=self.on_release)
    def start(self):
        self.keyboard_callback.start()
    def stop(self):
        self.keyboard_callback.stop()