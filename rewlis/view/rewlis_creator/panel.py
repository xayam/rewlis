from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget


class Panel(AnchorLayout):

    def __init__(self, anchor_x, anchor_y, **kwargs):
        AnchorLayout.__init__(self,
                              anchor_x=anchor_x, anchor_y=anchor_y,
                              size_hint=(0.1, 1),
                              **kwargs)
        self.gridlayout = None
        self.scrollview = None

    def init(self):
        self.scrollview = ScrollView(do_scroll_y=True, do_scroll_x=False)
        self.gridlayout = GridLayout(cols=1,
                                     size_hint=(1, None),
                                     padding=[140, 15],
                                     spacing=[140])
        for i in range(20):
            btn = Button(text=str(i))
            self.gridlayout.add_widget(btn)
        self.scrollview.add_widget(self.gridlayout)
        self.add_widget(self.scrollview)
        return self
