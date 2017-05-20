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

Builder.load_file('game/cities/cities.kv')
               
#main screen class contains the game
class City(Widget):
    pos = ListProperty([0, 0])
    size_x = NumericProperty(0)
    size_y = NumericProperty(0)
    
    def __init__(self, x, y, size_x, size_y, *args, **kwargs):
        super(City, self).__init__(*args, **kwargs)
        self.size_x = size_x
        self.size_y = size_y
        self.pos = x, y
        
        