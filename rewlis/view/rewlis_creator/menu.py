import threading

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


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
        btn = Button(text="RUN",
                     size_hint=(1, None),
                     size=(1, 95),
                     background_color=(1., 1., 0., 1.),
                     on_release=self.run_process)
        self.gridlayout.add_widget(btn)
        btn = Button(text="PREVIEW",
                     size_hint=(1, None),
                     size=(1, 95),
                     background_color=(1., 1., 0., 1.))
        self.gridlayout.add_widget(btn)
        btn = Button(text="SHARE",
                     size_hint=(1, None),
                     size=(1, 95),
                     background_color=(1., 1., 0., 1.))
        self.gridlayout.add_widget(btn)
        self.add_widget(self.gridlayout)
        return self

    def run_process(self, _):
        print("Running process of create sync-book...")
        t = threading.Thread(
            target=self.controller.creator.process,
            args=(self.controller.terminal.cprint,),
        )
        t.start()
