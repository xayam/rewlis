from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget


class Menu(AnchorLayout):

    def __init__(self, controller, **kwargs):
        AnchorLayout.__init__(self,
                              size_hint=(None, 1),
                              size=(95, 1),
                              anchor_y="top",
                              **kwargs)
        self.gridlayout = None
        self.scrollview = None
        self.controller = controller
        self.model = self.controller.model

    def init(self):
        self.gridlayout = GridLayout(cols=1,
                                     size_hint=(1, None),
                                     padding=[5, 5],
                                     spacing=[1])
        btn = Button(text="REFRESH", size_hint=(1, None), size=(1, 95))
        self.gridlayout.add_widget(btn)
        btn = Button(text="ADD", size_hint=(1, None), size=(1, 95))
        self.gridlayout.add_widget(btn)
        btn = Button(text="PROCESS", size_hint=(1, None), size=(1, 95))
        self.gridlayout.add_widget(btn)
        btn = Button(text="PREVIEW", size_hint=(1, None), size=(1, 95))
        self.gridlayout.add_widget(btn)
        btn = Button(text="ZIPPED", size_hint=(1, None), size=(1, 95))
        self.gridlayout.add_widget(btn)
        btn = Button(text="SHARE", size_hint=(1, None), size=(1, 95))
        self.gridlayout.add_widget(btn)
        self.add_widget(self.gridlayout)
        return self
