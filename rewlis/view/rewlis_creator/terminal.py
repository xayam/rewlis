import sys

from kivy.uix.textinput import TextInput

from rewlis.entity import *


class Terminal(TextInput):

    def __init__(self, model, **kwargs):
        self.model = model
        self.controller = self.model.controller
        super().__init__(
            size_hint=(1, 1),
            padding=(10, 10),
            focus=False,
            use_bubble=False,
            use_handles=False,
            scroll_from_swipe=False,
            selection_color=self.model.opt[SEL],
            background_color=self.model.opt[BG],
            foreground_color=self.model.opt[FG],
            **kwargs
        )
        self.stdout = sys.stdout
        self.is_focusable = True

    def write(self, message):
        self.text = self.text + message
        self.stdout.write(message)
        self.stdout.flush()

    def flush(self):
        pass
