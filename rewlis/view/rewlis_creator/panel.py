from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget


class Panel(AnchorLayout):

    def __init__(self, controller, **kwargs):
        AnchorLayout.__init__(self,
                              size_hint=(0.33, 1),
                              **kwargs)
        self.gridlayout = None
        self.scrollview = None
        self.controller = controller
        self.model = self.controller.model

    def init(self):
        self.scrollview = ScrollView(do_scroll_y=True,
                                     do_scroll_x=False)
        self.gridlayout = GridLayout(cols=1,
                                     size_hint=(1, None),
                                     padding=[10, 5],
                                     spacing=[5])
        for book in self.controller.creator.folder_of_books:
            btn = Button(text=book)
            self.gridlayout.add_widget(btn)
        self.gridlayout.size = 1, 30 * len(self.controller.creator.folder_of_books)
        self.scrollview.add_widget(self.gridlayout)
        self.add_widget(self.scrollview)
        return self
