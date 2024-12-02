import os.path

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from rewlis.entity import RESULT_VALID


class Panel(AnchorLayout):

    def __init__(self, controller, **kwargs):
        AnchorLayout.__init__(self,
                              size_hint=(None, 1),
                              size=(500, 1),
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
        for book, lang in self.controller.creator.folder_of_books:
            btn = Button(text=f"{lang}/{book}",
                         on_release=self.load,
                         )
            self.gridlayout.add_widget(btn)
        self.gridlayout.size = \
            1, 50 * len(self.controller.creator.folder_of_books)
        self.scrollview.add_widget(self.gridlayout)
        self.add_widget(self.scrollview)
        self.check_valid()
        return self

    def load(self, button):
        self.controller.project.load_project(
            book=button.text,
            current=self.model.conf.FOLDER_CREATE + "/" + button.text
        )

    def check_valid(self, _=None):
        for w in self.gridlayout.children:
            if os.path.exists(
                    f"{self.controller.creator.data}/sync{w.text[3:]}/{RESULT_VALID}"
            ):
                bgc = (0., 0., 1., 1.)
            elif os.path.exists(
                    f"{self.controller.creator.data}/{w.text}/{RESULT_VALID}"
            ):
                bgc = (0., 1., 0., 1.)
            else:
                bgc = (1., 0., 0., 1.)
            w.background_color = bgc

    def check_valid_sync(self, _=None):
        for w in self.gridlayout.children:
            if os.path.exists(
                    f"{self.controller.creator.data}/sync{w.text[3:]}/{RESULT_VALID}"
            ):
                w.background_color = (0., 0., 1., 1.)
