import kivy
kivy.require('1.8.1')

from kivy.app import App
from kivy.lang import Builder

root = Builder.load_string('''
BoxLayout:
    orientation: 'horizontal'
    BoxLayout:
        orientation: 'vertical'
        Splitter:
            sizable_from: 'bottom'
            Label:
                text: 'Graph'
        Label:
            text: 'Map'
    Splitter:
        sizable_from: 'left'
        layout_content: layout_content
        BoxLayout:
            id: bl
            orientation: 'vertical'
            padding: 50, 40
            row_default_height: '48dp'
            row_force_default: True
            spacing: 10, 10
            ScrollView:
                size: self.size
                GridLayout:
                    id: layout_content
                    size_hint_y: None
                    cols: 1
                    row_default_height: '20dp'
                    row_force_default: True
                    spacing: 0, 5
                    padding: 0, 0
                    height: self.minimum_height
                    
                    Button:
                        text: 'Data Set a'
                    Button:
                        text: 'Data Set b'
                    Button:
                        text: 'Data Set c'
                    Button:
                        text: 'Data Set d'
                    Button:
                        text: 'Data Set e'
                    Button:
                        text: 'Data Set f'
                    Button:
                        text: 'Data Set g'
                    Button:
                        text: 'Data Set h'
                    Button:
                        text: 'Data Set i'
                    Button:
                        text: 'Data Set j'
                    Button:
                        text: 'Data Set k'
                    Button:
                        text: 'Data Set l'
                    Button:
                        text: 'Data Set m'
                    Button:
                        text: 'Data Set n'
                    Button:
                        text: 'Data Set o'
                    Button:
                        text: 'Data Set p'
                    Button:
                        text: 'Data Set q'
                    Button:
                        text: 'Data Set r'
                    Button:
                        text: 'Data Set s'
                    Button:
                        text: 'Data Set t'
                    Button:
                        text: 'Data Set u'
                    Button:
                        text: 'Data Set v'
                    Button:
                        text: 'Data Set w'
                    Button:
                        text: 'Data Set x'
                    Button:
                        text: 'Data Set y'
                    Button:
                        text: 'Data Set z'
''')

class TestApp(App):
    def build(self):
        return root

if __name__ == '__main__':
    TestApp().run()