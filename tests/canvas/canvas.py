from kivy.app import App
from kivy.lang import Builder

class MyPaintApp(App):
    def build(self):
        b = Builder.load_file("tests/canvas/canvas.kv")
        return b

if __name__ == '__main__':
    MyPaintApp().run()
