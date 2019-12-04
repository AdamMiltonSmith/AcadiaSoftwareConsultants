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
                    
                    Button:
                        text: 'Data Set x'
                    Button:
                        text: 'Data Set x'
                    Button:
                        text: 'Data Set x'
                    Button:
                        text: 'Data Set x'
                    Button:
                        text: 'Data Set x'
                    Button:
                        text: 'Data Set x'
                    Button:
                        text: 'Data Set x'
                    Button:
                        text: 'Data Set x'
                    Button:
                        text: 'Data Set x'
                    Button:
                        text: 'Data Set x'
                    Button:
                        text: 'Data Set x'
                    Button:
                        text: 'Data Set x'
                    Button:
                        text: 'Data Set x'
                    Button:
                        text: 'Data Set x'
                    Button:
                        text: 'Data Set x'
                    Button:
                        text: 'Data Set x'
                    Button:
                        text: 'Data Set x'
                    Button:
                        text: 'Data Set x'
                    Button:
                        text: 'Data Set x'
                    Button:
                        text: 'Data Set x'
                    Button:
                        text: 'Data Set x'
                    Button:
                        text: 'Data Set x'
                    Button:
                        text: 'Data Set x'
                    Button:
                        text: 'ass'
''')

class TestApp(App):
    def build(self):
        return root

if __name__ == '__main__':
    TestApp().run()