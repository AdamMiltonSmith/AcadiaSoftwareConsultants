from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.properties import ObjectProperty, NumericProperty
from os import listdir
from os.path import isfile, join
import glob
import os

# some code I found online and have been messing with
class MyScreenManager(ScreenManager):
    total_button = NumericProperty(3)


class Login(Screen):
    login = ObjectProperty(None)

    def on_pre_enter(self):
        Window.size = (400, 300)

    def check_password(self, instance, password):
        if password == "pwd":
            instance.current = "registers"



class Registers(Screen):
    container = ObjectProperty(None)

    def on_enter(self):
        Window.size = (800, 600)


    def add_buttons(self):
        datasetPath = "resources\\csv_data_collection"
        files = listdir(datasetPath)
        for f in files:
            self.container.add_widget(Button(text=f, id=str(f)))

    def remove_buttons(self):
        for child in [child for child in self.container.children]:
            self.container.remove_widget(child)



class Welcome(Screen):
    pass


class TestApp(App):
    title = "Xd"

    def build(self):
        return MyScreenManager()


if __name__ == "__main__":
    TestApp().run()