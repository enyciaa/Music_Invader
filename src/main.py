'''
Main entry point for app
Does everything needed before the app starts up
Handles a lot of the behind the scene stuff, setting up app, acting as singleton, setting up services etc.

logic is that the this entry point opens ocean drops (UI manager) which creates the main menu
    
Added

To Do

Future

Widget Tree

       
'''
from __future__ import division

__version__ = '1.0.1'

import kivy
kivy.require('1.8.0')

#code to set window size on desktop
from kivy.config import Config
#display
#480, 800, 35, 1045
Config.set('graphics', 'width', '1136')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'top', '35')
Config.set('graphics', 'left', '350')
#modules
#Config.set('modules', 'touchring', '')
#Config.set('modules', 'monitor', '')
#Config.set('modules', 'keybinding', '')
#Config.set('modules', 'recorder', '')
#Config.set('modules', 'screen', '')
#Config.set('modules', 'inspector', '')
#Config.set('modules', 'webdebugger', '')

from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, \
    BooleanProperty, ReferenceListProperty, StringProperty
import threading
import json
from game import game
from library.button import lib_button
from library.text import lib_text
from game.enemies import midi_logic

app = None  
MY_LOCK = threading.Lock() #stops errors casued by multiple threads changing the same value
     

#sub thread continually checks if stop is set
#once it has been set thread exits        
class StoppableThread(threading.Thread):

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self.stop_event = threading.Event()
    
    #sets stop flag
    def stop(self):
        self.stop_event.set()
    
    #returns flag to thread
    def stopped_test(self):
        return self.stop_event.isSet()
    
    
#app entry point, setting everything up, handling services and acting as singleton
class MainApp(App):
    game = ObjectProperty(None)
    midi_thread = ObjectProperty(None)
    callback_queue = ObjectProperty(None)

    #json files
    game_layout = ObjectProperty(None)
    lib_text_layout = ObjectProperty(None)
    lib_button_layout = ObjectProperty(None)
    
    def build(self):         
        self.load_json_files()
        
        #app entry point
        global app
        app = self
        lib_button.app = self
        lib_text.app = self
        
        #ocean drops loading (includes app_switcher - the overall screen manager)
        game.app = self
        self.game = game.Game()
        self.game.start()
        
        return self.game
    
    #loads json files
    #can make this more sexy somehow
    def load_json_files(self):
        json_data = open('game/game.json')
        self.game_layout = json.load(json_data)
        json_data.close()
        
        json_data = open('library/button/lib_button.json')
        self.lib_button_layout = json.load(json_data)
        json_data.close()
        
        json_data = open('library/text/lib_text.json')
        self.lib_text_layout = json.load(json_data)
        json_data.close()            
           
    #runs straight after build
    def on_start(self):
        self.game.after_build()
        Window.bind(on_keyboard = self.android_back)
        self.play_midi()   
    
    #keeps the app open if the phone sleeps or switches app
    def on_pause(self):
        pass
        #return True     #disable when testing on kivy launcher
          
    #when app resumes put any data that needs reloaded here (if any)
    def on_resume(self):
        pass
    
    def on_stop(self):
        #wont work if thread isnt already running
        try:
            self.midi_thread.stop()    #stops midi thread, runs stop function to give thread flag indicating to stop
        except:    
            print 'midi_thread is not running and cant be stopped'
    
    #starts midi song in new thread        
    def play_midi(self):
        midi = midi_logic.MIDILogic()
        self.midi_thread = StoppableThread(target=midi.play, args=())
        self.midi_thread.start() 
    
    #code to run when android back button (or keyboard escape button) is pressed
    def android_back(self, window, key, *args):
        if key == 27:        #key 27 is the esc key or back button on android
            #code describing what key should do
            return True
        
        
if __name__ == '__main__':
    MainApp().run()