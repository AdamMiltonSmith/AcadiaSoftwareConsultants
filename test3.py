from kivy.lang import Builder
from kivy.factory import Factory
from kivymd.app import MDApp

Builder.load_string(
    """
<ExampleButtons@BoxLayout>:
    orientation: "vertical"

    TextInput:
        text: "Hello"
        multiline: False
        size: 75, 50
        size_hint: None, None
"""
)


class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "KivyMD Examples - Buttons"
        self.theme_cls.primary_palette = "Blue"
        super().__init__(**kwargs)

    def build(self):
        self.root = Factory.ExampleButtons()


if __name__ == "__main__":
    MainApp().run()
