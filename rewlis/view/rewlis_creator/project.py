from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget


class Project(AnchorLayout):

    def __init__(self, controller, **kwargs):
        AnchorLayout.__init__(self, **kwargs)
        self.controller = controller
        self.model = self.controller.model


    def init(self):
        return self
