'''
Contains the game screen
    
Added

To Do

Future

Widget Tree
       
'''

from __future__ import division
from kivy.app import Builder
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, \
    BooleanProperty, ReferenceListProperty, StringProperty
from random import randrange
from cities import cities
from defense import defense
from enemies import enemies

Builder.load_file('game/game.kv')

app = None  
game = None

#draws projectiles
class Defense(Widget):
    defenders = ListProperty([])
    
    def draw_projectile(self, touch, velocity):
        size_x = Window.width * 0.03
        size_y = Window.height * 0.05
        #start position of bullet is the top of the turret
        x = Window.width * 0.5 - (size_x / 2)
        y = Window.height * 0.1
        new_defender = defense.Projectile(x, y, size_x, size_y, touch.pos, velocity)
        self.defenders = self.defenders + [new_defender]    
        game.add_widget(new_defender)         
           
    def update(self):
        for defender in self.defenders:
            if defender.collide_widget(game) == False:   #checks if projectile is in window
                game.remove_widget(defender)
                self.defenders.remove(defender)    
            defender.update() 
            
#draws enemies            
class Attackers(Widget):
    attackers = ListProperty([])
    segment_length = NumericProperty(0)
    
    def segment_setter(self):
        self.segment_setter = Window.width / 12
    
    def draw_attacker(self):
        size_x = Window.width * 0.07
        size_y = Window.height * 0.07
        x = self.x_position(size_x)
        y = Window.height
        enemy_number = 'enemy' + str(game.enemy_type)
        new_attacker = enemies.Attacker(x, y, size_x, size_y, enemy_number)
        self.attackers = self.attackers + [new_attacker]      #adds a reference of attacker to list so its accessible
        game.add_widget(new_attacker)
   
    #assigns the enemys a random position in one of 12 segments
    def x_position(self, size_x):
        right = self.segment_setter * game.enemy_type
        right = right + self.segment_setter
        right = right - size_x
        left = self.segment_setter * game.enemy_type
        if left > right:
            left = right - 2    
        x = randrange(int(left), int(right), 1) 
        return x
    
    def update(self):
        for attacker in self.attackers:
            if attacker.collide_widget(game) == False:   #checks if attacker is in game window
                game.remove_widget(attacker)
                self.attackers.remove(attacker)
            attacker.update()  
        
        
#draws cities and turret      
class Foreground(Widget):
    
    def draw(self):
        self.city_position()
        self.turret_position()
    
    def city_position(self):
        #sizeing
        size_x = Window.width * 0.2
        size_y = Window.height * 0.1
        #positioning
        x1 = Window.width * 0.2 - (size_x / 2)
        y1 = Window.height * 0
        x2 = Window.width * 0.8 - (size_x / 2)
        y2 = Window.height * 0
        #add widget
        game.add_widget(cities.City(x1, y1, size_x, size_y))
        game.add_widget(cities.City(x2, y2, size_x, size_y))
        
    def turret_position(self):
        size_x = Window.width * 0.2
        size_y = Window.height * 0.1
        x = Window.width * 0.5 - size_x / 2
        y = Window.height * 0
        game.add_widget(defense.Turret(x, y, size_x, size_y))    
                        
                                              
class GameState(Widget):
    game_state = BooleanProperty(False)
    
    def test(self):
        pass
    
    def start_game(self):
        Clock.schedule_interval(game.update, 1/game.fps_normal)
        self.game_state = True
    
    def end_game(self):
        Clock.unschedule(game.update)
        self.game_state = False
        
               
#main screen class contains the game
class Game(Widget):
    game_state = ObjectProperty(None)
    foreground = ObjectProperty(None)
    attackers = ObjectProperty(None)
    defense = ObjectProperty(None)
    
    touch_time = 0
    draw_enemy = False
    enemy_type = 0
    fps_normal = 60
    fps_adj_factor = 0
        
    def start(self):
        global game
        game = self
        self.game_state = GameState()
        self.foreground = Foreground()
        self.attackers = Attackers()
        self.defense = Defense()
        self.foreground.draw()
    
    #runs on_start of app
    def after_build(self):
        self.attackers.segment_setter()
        self.game_state.start_game()
    
    #not used yet, but this should help keep movement constant over varying fps's
    def fps(self):
        self.fps_current = Clock.get_rfps()
        if self.fps_current == 0:   #to prevent division by zero error
            self.fps_current = self.fps_normal
        self.fps_adj_factor = self.fps_normal / float(self.fps_current) 
    
    #registers initial touch for projectile
    def on_touch_down(self, touch):
        self.touch_time = Clock.get_boottime()
    
    #calculates the velocity of projectile
    def calc_velocity(self):
        self.touch_time = Clock.get_boottime() - self.touch_time
        self.touch_time = self.touch_time * 35
        if self.touch_time < 2:    #creates a minimum velocity
            self.touch_time = 15
        if self.touch_time > 25:    #creates a maximum velocity
            self.touch_time = 25  
    
    #draws projectile on touch up
    def on_touch_up(self, touch):
        self.calc_velocity()
        self.defense.draw_projectile(touch, self.touch_time)
        self.touch_time = 0
    
    #removes collided objects
    def collision_remove(self, defender, attacker):
        try:
            #this can give an 'already remove' error not sure why
            if defender.collide_widget(attacker):
                game.remove_widget(defender)
                self.defense.defenders.remove(defender)  
                game.remove_widget(attacker)
                self.attackers.attackers.remove(attacker)            
        except:
            pass
        
    #checks for collisions between projectiles and attackers    
    def collision(self):
        for defender in self.defense.defenders:
            for attacker in self.attackers.attackers:
                self.collision_remove(defender, attacker)
    
    #draws enemy if flags have been altered by sub thread
    #need a direct way of calling the draw attacker function
    def draw_enemy_test(self):
        if self.draw_enemy:
            self.attackers.draw_attacker()
            self.draw_enemy = False
    
    #main update function    
    def update(self, dt):
        if self.game_state:
            self.fps()
            self.game_state.test()
            self.collision() 
            self.draw_enemy_test()
            self.attackers.update()
            self.defense.update()