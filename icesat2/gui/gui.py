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
from math import sin
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty  
from kivy.clock import Clock
#from icesat2.gui import graph
from os import listdir
from os.path import isfile, join
import glob
import os



def pre_init_screen():
    import tkinter as tk

    screen = tk.Tk()

    screenx, screeny = screen.winfo_screenwidth(), screen.winfo_screenheight()

class MainApp(App):
   
    assigned = False
    carrot = ObjectProperty(None)
    def build(self):
        self.title = "IGLOO"
        b = Builder.load_file("icesat2\\gui\\kv\\gui.kv")


        #Clock.schedule_interval(self.update, 1)
        return b
    
    # def update(self, *args):
    #     print("test")
        
    # def assign(self, booten):
    #     if assigned == False:
    #         print("<Assigning Shit")
    #         carrot = booten
    #         assigned = True
    #         carrot.doTheThing()
        
        


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

class DataSetRefreshButton(Button):
    font_size = prop.NumericProperty(14)
    back_color = prop.ColorProperty([0.5, 0.5, 0.5, 1.0])

    text_color = prop.ColorProperty([1.0, 1.0, 1.0, 1.0])
    btn_height = prop.NumericProperty(20)
    #btn_width = prop.NumericProperty(70)
    side_width_buffer = prop.NumericProperty(20)

    container = ObjectProperty(None) #container the buttons are added to
    def add_buttons(self):
        datasetPath = "resources"
        #files = listdir(datasetPath)
        files = next(os.walk(datasetPath))[1]
        print(files)
        for f in files:
            tempButton = DefaultButton()
            tempButton.text = f
            self.container.add_widget(tempButton)
    #remove buttons
    def remove_buttons(self):
        for child in [child for child in self.container.children]:
                self.container.remove_widget(child)
    def doTheThing(self):
        print("Doing the thing")


class Main_Window(Screen):
    def __init__(self, **kw):
        super(Main_Window, self).__init__(**kw)

class Graph_Window(Screen):
    def __init__(self, **kw):
        super(Graph_Window, self).__init__(**kw)

class Map_Window(Screen):
    def __init__(self, **kw):
        super(Map_Window, self).__init__(**kw)

class ScreenManagement(ScreenManager):
    pre_init_screen()
    pass

class WindowSplitter(Splitter):
    border_size = prop.NumericProperty(5)

class SetGraph(Widget):
    testGraph = ObjectProperty(None)

# sm = ScreenManager()

# screens = [Main_Window(name='main')]

# for screen in screens:
#     sm.add_widget(screen)

# sm.current = 'main'


def main():
    MainApp().run()
