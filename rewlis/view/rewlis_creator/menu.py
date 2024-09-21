from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget


class Menu(AnchorLayout):

    def __init__(self, **kwargs):
        AnchorLayout.__init__(self,
                              size_hint=(0.1, 1),
                              **kwargs)
        self.gridlayout = None
        self.scrollview = None

    def init(self):
        self.gridlayout = GridLayout(cols=1,
                                     size_hint=(1, None),
                                     padding=[0, 0],
                                     spacing=[0])
        btn = Button(text="Add...")
        self.gridlayout.add_widget(btn)
        btn = Button(text="Refresh")
        self.gridlayout.add_widget(btn)
        self.add_widget(self.gridlayout)
        return self
