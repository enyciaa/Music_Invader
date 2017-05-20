'''
Contains the game screen
    
Added

To Do

Future

Widget Tree
       
'''

from kivy.app import Builder
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, \
    BooleanProperty, ReferenceListProperty, StringProperty

Builder.load_file('game/enemies/enemies.kv')
    
#main screen class contains the game
class Attacker(Widget):
    size_x = NumericProperty(0)
    size_y = NumericProperty(0)
    pos = ListProperty([0, 0])
    source_image = StringProperty('assets/game/enemies/enemy0.png')
    
    velocity_y = 1.5
    
    def __init__(self, x, y, size_x, size_y, enemy_number, *args, **kwargs):
        super(Attacker, self).__init__(*args, **kwargs)
        self.size_x = size_x
        self.size_y = size_y 
        self.pos = x, y
        self.picture_source(enemy_number)
    
    #updates which enemies picture is used
    def picture_source(self, enemy_number):
        folder = 'assets/game/enemies/' 
        png = '.png'
        self.source_image = folder + enemy_number + png
        
    def update(self):
        self.pos[1] = self.pos[1] - self.velocity_y   #changes y co-ordinate of pos