import kivy
kivy.require('1.8.1')

from kivy.app import App
from kivy.lang import Builder
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
import ctypes


root = Builder.load_file("icesat2\\gui\\kv\\resizable.kv")

class ObamasAsshole(Button):
    self.text = "ur mom"

class Touch(BoxLayout):


    def __init__(self, **kwargs):
        super(Touch, self).__init__(**kwargs)
        
        
        self.selectBox = True
        self.orientation = 'vertical'
        self.picture = Image(allow_stretch=True, source='resources\\map_images\\ice_field_map2.TIF')
        #Clock.schedule_once(lambda dt: self.add_widget(self.picture), timeout=0.1)
        self.add_widget(self.picture)
       

  
        #draw a rectangle
        with self.canvas:
            Color(1,0,0,.5,mode='rgba')
            self.rect = Rectangle(pos=(0,0), size=(0,0))
        

        self.bottomBox = BoxLayout(orientation = 'horizontal')
        self.bottomBox.height = 100
        toggleButton = Button(text = 'Toggle Bounding Box Select')
        textinput = TextInput(text='Hi')
        self.bottomBox.add_widget(textinput)
        self.bottomBox.add_widget(toggleButton)
 
        self.add_widget(self.bottomBox)


    def on_touch_down(self, touch):
        self.rect.pos = touch.pos
        self.rect.size = (1, 1)

    def on_touch_move(self, touch):
        self.rect.size = (touch.x - touch.ox, touch.y - touch.oy)
    
    
    def set_box_pos(self,x,y):
        self.rect.pos = (x,y)

    def _on_keyboard_down(self):
        print("keydown")

class TestApp(App):
    def build(self):
        return root

if __name__ == '__main__':
    TestApp().run()