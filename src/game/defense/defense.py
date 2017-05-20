'''
Contains the game screen
    
Added

To Do

Future

Widget Tree
       
'''

from kivy.app import Builder
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.vector import Vector
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, \
    BooleanProperty, ReferenceListProperty, StringProperty
import math

Builder.load_file('game/defense/defense.kv')
    
#main screen class contains the game
class Turret(FloatLayout):
    size_x = NumericProperty(0)
    size_y = NumericProperty(0)
    pos = ListProperty([0, 0])
    
    def __init__(self, x, y, size_x, size_y, *args, **kwargs):
        super(Turret, self).__init__(*args, **kwargs)
        self.size_x = size_x
        self.size_y = size_y
        self.pos = x, y
        

class Projectile(FloatLayout):  
    size_x = NumericProperty(0)
    size_y = NumericProperty(0)
    pos = ListProperty([0, 0])
    touch_pos = [0, 0]
    
    timestep = 0.01
    gravity = (0, -0.2)
    velocity = 0
    
    def __init__(self, x, y, size_x, size_y, touch, velocity, *args, **kwargs):
        super(Projectile, self).__init__(*args, **kwargs)
        self.size_x = size_x
        self.size_y = size_y 
        self.pos = x, y
        self.touch_pos = touch
        self.velocity = velocity
        self.move_vector(self.pos, self.touch_pos, self.velocity)
      
    #see http://noobtuts.com/python/vector for further explanation
    def sub(self, u, v):
        #zip(u, v) makes [(x, y), (x, y)]
        return [a - b for a, b in zip(u, v)]
    
    def length_squared(self, u):
        return sum([a ** 2 for a in u])

    def length(self, u):
        return math.sqrt(self.length_squared(u))
    
    def scale_by_scalar(self, u, scalar):
        return [a * scalar for a in u]
    
    def setlength(self, u, l):
        return self.scale_by_scalar(u, l / self.length(u))
    
    def add(self, u, v):    
        return [a + b for a, b in zip(u, v)]
    
    def move_vector(self, pos, touch, velocity):
        'simplify using http://kivy.org/docs/api-kivy.vector.html'
        self.move_vector = self.sub(touch, pos)
        self.move_vector = self.setlength(self.move_vector, velocity)
    
    def update(self):
        self.timestep += 0.008
        gravity = Vector(self.gravity) * self.timestep
        self.move_vector = self.add(self.move_vector, gravity)
        self.pos = self.add(self.pos, self.move_vector)
        
        
        