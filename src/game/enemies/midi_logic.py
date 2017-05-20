'''
Contains the game screen
    
Added

To Do

Future


Widget Tree
       
'''
from __future__ import division

import math
import mido
from mido import MidiFile
import __main__    #not the best solution but as theres only one entry point for app it works fine

class MIDILogic():
    
    #plays midi file
    def play(self):
        port_name = 'Microsoft GS Wavetable Synth'    #will need to pick up which port to use when used on different devices
        filename = 'assets/game/enemies/level_1.MID'    #use this to set which level is played
        
        mido.set_backend('mido.backends.pygame')
        with mido.open_output(port_name) as output:
            with MidiFile(filename) as midi_file:
                for message in midi_file.play():
                    if __main__.app.midi_thread.stopped_test():   #checks for stop thread flag
                        break
                    byte_message = message.bytes()
                    self.spawn_enemy(byte_message)
                    output.send(message) 
    
    #tells main thread to draw the enemy type                
    def spawn_enemy(self, byte_message):
        if byte_message[0] == 144:   #if note message is 'note off'
            enemy_key = byte_message[1]
            enemy_key = ((enemy_key / 12) - math.trunc(enemy_key / 12)) * 12  #gets the note number (1-12)
            enemy_key = round(enemy_key)
            enemy_key = int(enemy_key)   #for some reason need round and int or it doesn't get the right note number
            __main__.MY_LOCK.acquire()   #locks these variables to the sub thread, i.e main thread can't alter them
            __main__.app.game.enemy_type = enemy_key
            __main__.app.game.draw_enemy = True
            __main__.MY_LOCK.release()
        