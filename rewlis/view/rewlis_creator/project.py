from kivy.uix.button import Button
from kivy.uix.widget import Widget


class Project(Button):

    def __init__(self, **kwargs):
        Button.__init__(self, **kwargs)


    def init(self):
        return self
