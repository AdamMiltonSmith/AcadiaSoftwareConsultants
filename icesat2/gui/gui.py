import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager


class MainApp(App):
    def build(self):
        self.title = "IGLOO"
        return sm


class FileDropDown(DropDown):
    pass


class Main_Window(Screen):
    pass


Builder.load_file("icesat2\\gui\\kv\\gui.kv")

sm = ScreenManager()

screens = [Main_Window(name='main')]

for screen in screens:
    sm.add_widget(screen)

sm.current = 'main'


def main():
    MainApp().run()
