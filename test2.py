from kivy.lang import Builder
from kivy.base import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
Builder.load_string('''
<Test>:
    orientation: 'vertical'
    Button:
        text: 'hide'
        on_release: root.hide(box)
    BoxLayout:
        id: box
        Button:
            text: 'Hi %s!' % self.parent
    Button
        text: 'Retrieve'
        on_release: root.hide(root.placeholder, root.saved)
''')


class Test(BoxLayout):
    def hide(self, what, retrieve=None):
        # you'll need that object accessible and ".parent" will disappear
        parent = what.parent
        children = what.parent.children[:]

        # check for position in children list
        place = children.index(what)

        # save the widget you want to hide
        self.saved = children[place]

        # save children from the latest added to the removed one
        saved_children = children[0:place+1]

        # sizes are optional here
        self.placeholder = Widget(size_hint=[None, None],
                                  size=saved_children[0].size)
        for child in saved_children:
            parent.remove_widget(child)  # here you still can use what.parent

        # here the ".parent" is not available - the reason for "parent" var.
        # add Widget instead of whatever you will "hide"
        # pass to "retrieve" the saved widget if you want it back
        parent.add_widget(self.placeholder if not retrieve else retrieve)

        # add widgets in order they were originally added to the parent
        for child in list(reversed(saved_children[:place])):
            parent.add_widget(child)
        # cleanup mess ^^
        del children, saved_children


runTouchApp(Test())
