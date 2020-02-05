import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.splitter import Splitter
from kivy.core.window import Window
import kivy.properties as prop
from kivy.config import Config
#from icesat2.gui import graph


def pre_init_screen():
    import tkinter as tk
    
    screen = tk.Tk()
    
    screenx, screeny = screen.winfo_screenwidth(), screen.winfo_screenheight()

class MainApp(App):
    def build(self):
        self.title = "IGLOO"

        b = Builder.load_file("icesat2\\gui\\kv\\gui.kv")

        return b


class TopButton(Button):
    font_size = prop.NumericProperty(14)
    back_color = prop.ColorProperty([0.9, 0.9, 0.9, 1.0])
    #back_normal = prop.ColorProperty([1.0, 1.0, 1.0, 1.0])
    text_color = prop.ColorProperty([0.0, 0.0, 0.0, 1.0])
    btn_height = prop.NumericProperty(35)
    btn_width = prop.NumericProperty(70)
    side_width_buffer = prop.NumericProperty(20)


class TopButtonDropDown(DropDown):
    font_size = prop.NumericProperty(14)


class TopButtonDropDownButton(Button):
    font_size = prop.NumericProperty(14)
    back_color = prop.ListProperty([0.9, 0.9, 0.9, 1.0])
    back_normal = prop.ListProperty([0.0, 0.0, 0.0, 1.0])
    btn_height = prop.NumericProperty(35)
    btn_width = prop.NumericProperty(70)
    side_width_buffer = prop.NumericProperty(20)


class DefaultButton(Button):
    font_size = prop.NumericProperty(14)
    back_color = prop.ColorProperty([0.5, 0.5, 0.5, 1.0])

    text_color = prop.ColorProperty([1.0, 1.0, 1.0, 1.0])
    btn_height = prop.NumericProperty(20)
    #btn_width = prop.NumericProperty(70)
    side_width_buffer = prop.NumericProperty(20)


class Main_Window(Screen):
    def __init__(self, **kw):
        super(Main_Window, self).__init__(**kw)
        
class Graph_Window(Screen):
    def __init__(self, **kw):
        super(Graph_Window, self).__init__(**kw)


class ScreenManagement(ScreenManager):
    pre_init_screen()
    pass

class WindowSplitter(Splitter):
    border_size = prop.NumericProperty(5)


# sm = ScreenManager()

# screens = [Main_Window(name='main')]

# for screen in screens:
#     sm.add_widget(screen)

# sm.current = 'main'


def main():
    MainApp().run()