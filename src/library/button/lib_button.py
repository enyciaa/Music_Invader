'''
Utility file with chunks of code used in whole package
Contains all the button templates

Added
-added button 13 (notifications)
-Made button normal color be taken from buttons original color.

To Do
-if label is smaller than button a click on the button won't highlight label as well, how to fix?


Future
-Having seperate button label and image seems complicated
    -See if this can be set in one widget (PIL text?)
    
'''

from kivy.app import Builder
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, \
    BooleanProperty, ReferenceListProperty, StringProperty    

Builder.load_file('library/button/lib_button.kv') 

app = None

#Template class for all button labels
class ButtonLabel(Label, ButtonBehavior):
    pressed_label = ObjectProperty(None, allownone = True)
    pressed_down = BooleanProperty(False)
    label_color = ListProperty([])
    
    #when label is clicked text becomes translucent        
    def click_down(self, label):
        self.pressed_down = True
        self.pressed_label = label
        self.label_color = label.color
        label.color = app.lib_button_layout["button_label"]["pressed_color"]

    #when touch moves off text, text returns to normal color    
    def click_moved(self, label):
        if self.pressed_down:
            self.pressed_label = None
            self.pressed_down = False
            label.color = self.label_color
            
    #on label click change label color back to original         
    def click_up(self, label):
        self.pressed_down = False
        if label == self.pressed_label:
            self.pressed_label = None
            label.color = self.label_color
            

#Template class for all buttons to give them desired clicking behaviour
class ButtonClicks(Image, ButtonBehavior):  
    pressed_button = ObjectProperty(None, allownone = True)
    pressed_down = BooleanProperty(False)
    button_color = ListProperty([])
    
    #when button is clicked text becomes translucent        
    def click_down(self, button):
        self.pressed_down = True
        self.pressed_button = button
        self.button_color = button.color
        button.color = app.lib_button_layout["button_clicks"]["pressed_color"]
    
    #when touch moves off text, text returns to normal color    
    def click_moved(self, button):
        if self.pressed_down:
            self.pressed_button = None
            self.pressed_down = False
            button.color = self.button_color
            
    #on button click start the game           
    def click_up(self, button, button_identifier):
        self.pressed_down = False
        if button == self.pressed_button:
            self.pressed_button = None
            button.color = self.button_color
            run_function = self.button_functions[button_identifier]
            exec run_function
    
    button_functions = {
            "but_001": "self.but_001()",
            "but_002": 'app.ocean_drops.title_bar.open_drop_down(button)',
            "but_003": "self.but_003()",
            "but_004": "app.three_drops.td_manager.current = 'ReadMore'",
            "but_005": "self.but_005()",
            "but_006": "app.three_drops.td_manager.current = 'Three'",
            "but_007": "app.three_drops.td_manager.current = 'StartScreen'",
            "but_008": "app.three_drops.td_manager.current = 'Sent'",
            "but_009": "app.three_drops.td_manager.current = 'Three'",
            "but_010": "self.but_010()",
            "but_011": "app.three_drops.td_manager.current = 'StartScreen'",
            "but_012": "self.but_012()",
            "but_013": "self.but_013()",
            "but_014": "app.misc.reminders.time_popup()"
        }
    
    #if multiple functions are run
    #the library directs the button press to one of these functions
    
    #home button
    def but_001(self):
        'kills app and cancels alarm manager schedule'
        'delete this before build'
        from android_integration import notificaitons
        scheduler = notificaitons.Scheduler()
        scheduler.cancel_schedule()
        app.stop()
        'delete this before build'
        app.ocean_drops.app_switcher.current = 'MainMenu'
        app.ocean_drops.title_bar.set_main_title()
    
    #menu button to enter three drops mini app
    def but_003(self):
        app.ocean_drops.app_switcher.current = 'ThreeDrops'
        mini_title = app.td_layout["whole_section"]["app_title"] 
        app.ocean_drops.title_bar.mini_app_title(mini_title)
        
    #back button on first screen of three drops
    def but_005(self):
        app.ocean_drops.app_switcher.current = 'MainMenu'
        app.ocean_drops.title_bar.set_main_title()
    
    #main menu button at the end of three drops
    def but_010(self):
        app.ocean_drops.app_switcher.current = 'MainMenu'
        app.three_drops.td_manager.current = 'StartScreen'
        app.ocean_drops.title_bar.set_main_title()
        
    #about button in title drop down
    def but_012(self):
        app.ocean_drops.app_switcher.current = 'Misc'
        app.misc.misc_manager.current = 'About'
        title = 'About'
        app.ocean_drops.title_bar.mini_app_title(title)
        app.ocean_drops.title_bar.title_drop.dismiss()  
        
    #reminders button in title drop down
    def but_013(self):
        app.ocean_drops.app_switcher.current = 'Misc'
        app.misc.misc_manager.current = 'Reminders'
        title = 'Reminders'
        app.ocean_drops.title_bar.mini_app_title(title)
        app.ocean_drops.title_bar.title_drop.dismiss()      