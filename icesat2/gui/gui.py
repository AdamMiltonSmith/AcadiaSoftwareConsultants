import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.splitter import Splitter
from kivy.core.window import Window
import kivy.properties as prop
#from icesat2.gui import graph
from os import listdir
from os.path import isfile, join
import glob
import os



# def pre_init_screen():
#     import sys


#     """
#     returns Monitor size x and y in pixels for desktop platforms, or None for
#     mobile platforms
#     Found at:
#     https://groups.google.com/forum/#!topic/kivy-users/uZYrghb87g0
#     """
#     if sys.platform == 'linux2':
#         import subprocess
#         output = subprocess.Popen(
#             'xrandr | grep "\*" | cut -d" " -f4',
#             shell=True,
#             stdout=subprocess.PIPE).communicate()[0]
#         screenx = int(output.replace('\n', '').split('x')[0])
#         screeny = int(output.replace('\n', '').split('x')[1])
#     elif sys.platform == 'win32':
#         from pywin32 import GetSystemMetrics
#         screenx = GetSystemMetrics(0)
#         screeny = GetSystemMetrics(1)
#     elif sys.platform == 'darwin':
#         from AppKit import NSScreen
#         frame_size = NSScreen.mainScreen().frame().size
#         return frame_size.width, frame_size.height
#     else:
#         # For mobile devices, use full screen
#         screenx, screeny = 800, 600  # return something

class MainApp(App):
    def build(self):
        self.title = "IGLOO"
        
        b = Builder.load_file("icesat2\\gui\\kv\\gui.kv")

        #Window.size = (1920, 1080)

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


    container = ObjectProperty(None) #container the buttons are added to
    def add_buttons(self):
        datasetPath = "resources\\csv_data_collection"
        files = listdir(datasetPath)
        print(files)
        for f in files:
            self.container.add_widget(Button(text=f, id=str(f)))

    # Currently, the refresh button gets replaced by a duplicate of the last button
    # after the first refresh
    def remove_buttons(self):
        skipfirst = 0 #prevents the refresh button from being removed
        for child in [child for child in self.container.children]:
            if skipfirst != 0:
                self.container.remove_widget(child)
            else:
                skipfirst += 1


class Main_Window(Screen):
    def __init__(self, **kw):
        super(Main_Window, self).__init__(**kw)

        
class Graph_Window(Screen):
    def __init__(self, **kw):
        super(Graph_Window, self).__init__(**kw)


class ScreenManagement(ScreenManager):
    #pre_init_screen()
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
