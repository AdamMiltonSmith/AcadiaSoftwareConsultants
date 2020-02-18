import glob
import os
from math import sin
#from icesat2.gui import graph
from os import listdir
from os.path import isfile, join

import kivy
import kivy.properties as prop
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.garden.mapview import MapView
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.splitter import Splitter
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
import re


def pre_init_screen():
    import tkinter as tk

    screen = tk.Tk()

    screenx, screeny = screen.winfo_screenwidth(), screen.winfo_screenheight()

class MainApp(App):

    assigned = False
    carrot = prop.ObjectProperty(None)
    def build(self):
        self.title = "IGLOO"
        b = Builder.load_file("icesat2\\gui\\kv\\gui.kv")


        Clock.schedule_interval(self.update, 1)
        return b

    def update(self, *args):
        pass

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


class CoordinateTextInput(TextInput):
    default_text = "Format xx.xx"
    default_shade = prop.ColorProperty([0.5, 0.5, 0.5, 1.0])

    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        """Disallows users from entering anything other than numbers into the
        boxes"""
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(CoordinateTextInput, self).insert_text(s, from_undo=from_undo)

    def on_enter(self):
        """Function that validates the data that the user just pressed enter
        with"""
        print('User pressed enter in', self, self.coord_dir)


    def check_text(self):
        """Function that will clear the text in the box and change the color
        of the text, more of a quality of life check and not necessary as of
        now"""
        #got focus
        if self.focus:
            pass
        #lost focus
        else:
            pass

class DateChooseButton(Button):
    font_size = prop.NumericProperty(12)
    back_color = prop.ColorProperty([0.9, 0.9, 0.9, 1.0])
    #back_normal = prop.ColorProperty([1.0, 1.0, 1.0, 1.0])
    text_color = prop.ColorProperty([0.0, 0.0, 0.0, 1.0])
    side_width_buffer = prop.NumericProperty(20)

    # def create_buttons(self, date_id, widget_id):
    #     dropdown = self.parent.ids.end_date_year_dropdown

    #     for index in range(10):
    #         btn = Button(text=f"{index}", size_hint_y=None, width = 40, height=25)

    #         btn.bind(on_release=lambda btn: dropdown.select(btn.text))

    #         dropdown.add_widget(btn)

    #     dropdown.bind(on_select=lambda instance, x: setattr(self, 'text', x))


class DayDD(DropDown):
    font_size = prop.NumericProperty(12)

    def create_buttons(self, date_id):
        dropdown = self

        for index in range(10):
            btn = Button(text=f"{index}", size_hint_y=None, width = 40, height=25)

            btn.bind(on_release=lambda btn: dropdown.select(btn.text))

            dropdown.add_widget(btn)

        dropdown.bind(on_select=lambda instance, x: setattr(self, 'text', x))


class MonthDD(DropDown):
    font_size = prop.NumericProperty(12)

    def create_buttons(self, date_id):
        dropdown = self

        for index in range(10):
            btn = Button(text=f"{index}", size_hint_y=None,
                         width=40, height=25)

            btn.bind(on_release=lambda btn: dropdown.select(btn.text))

            dropdown.add_widget(btn)

        dropdown.bind(on_select=lambda instance, x: setattr(self, 'text', x))

class YearDD(DropDown):
    font_size = prop.NumericProperty(12)

    def __init__(self, **kwargs):

        super(YearDD, self).__init__(**kwargs)

        #need to make these the button below, these need a lot of work
        for index in range(2018, 2023):
            btn = DateChooseDropDownButton(text=f"{index}", size_hint_y=None,
                         width=40, height=25, background_color = [0, 0, 0, 1.0], text_color = [0, 0, 0, 1.0], background_normal = '')

            btn.bind(on_release=lambda btn: self.set_and_dismiss(btn.text))

            self.add_widget(btn)
            
        #self.bind(on_select=lambda instance, x: setattr(self, 'text', x))

    def set_and_dismiss(self, value):
        self.parent_widget.text = value
        self.dismiss()


class DateChooseDropDownButton(Button):
    font_size = prop.NumericProperty(14)
    side_width_buffer = prop.NumericProperty(20)
    #back_color = prop.ColorProperty([0.9, 0.9, 0.9, 1.0])
    #back_normal = prop.ColorProperty([1.0, 1.0, 1.0, 1.0])
    text_color = prop.ColorProperty([0.0, 0.0, 0.0, 1.0])

class CoordinatePopup(Popup):
    def process_input(self):
        coord_input = []
        print(self.ids.popup_layout.children)
        for child in self.ids.popup_layout.children:
            if isinstance(child, CoordinateTextInput):
                coord_input.append(child)
        for widget in coord_input:
            print(widget.text)


class DataSetRefreshButton(Button):
    font_size = prop.NumericProperty(14)
    back_color = prop.ColorProperty([0.5, 0.5, 0.5, 1.0])

    text_color = prop.ColorProperty([1.0, 1.0, 1.0, 1.0])
    btn_height = prop.NumericProperty(20)
    #btn_width = prop.NumericProperty(70)
    side_width_buffer = prop.NumericProperty(20)

    container = prop.ObjectProperty(None) #container the buttons are added to
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

class Map(MapView):
    pass

class ScreenManagement(ScreenManager):
    pre_init_screen()
    pass

class WindowSplitter(Splitter):
    border_size = prop.NumericProperty(5)

class SetGraph(Widget):
    testGraph = prop.ObjectProperty(None)

# sm = ScreenManager()

# screens = [Main_Window(name='main')]

# for screen in screens:
#     sm.add_widget(screen)

# sm.current = 'main'


def main():
    MainApp().run()
