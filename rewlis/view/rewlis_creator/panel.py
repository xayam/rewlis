import os.path

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView


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
            if os.path.exists(
                self.controller.creator.data + "/" + book + "/" +
                self.model.conf.VALID
            ):
                bgc = (0., 1., 0., 1.)
            else:
                bgc = (1., 0., 0., 1.)
            btn = Button(text=book,
                         on_release=self.load,
                         background_color=bgc,
                         )
            self.gridlayout.add_widget(btn)
        self.gridlayout.size = \
            1, 50 * len(self.controller.creator.folder_of_books)
        self.scrollview.add_widget(self.gridlayout)
        self.add_widget(self.scrollview)
        return self

    def load(self, button):
        self.controller.project.load_project(
            book=button.text,
            current=self.model.conf.FOLDER_CREATE + "/" + button.text
        )
