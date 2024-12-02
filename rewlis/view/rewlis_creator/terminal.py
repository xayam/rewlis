import sys

from kivy.clock import Clock
from kivy.uix.textinput import TextInput


class Terminal(TextInput):

    def __init__(self, model, **kwargs):
        self.model = model
        self.controller = self.model.controller
        TextInput.__init__(
            self,
            size_hint=(1, 1),
            padding=(10, 10),
            focus=False,
            use_bubble=False,
            use_handles=False,
            scroll_from_swipe=False,
            selection_color=(1., 0., 0., 0.3),
            background_color=(1., 1., 1., 1.),
            foreground_color=(0., 0., 0., 1.),
            **kwargs
        )
        self.is_focusable = True


    def write(self, *args):
        message = " ".join(map(str, args))
        self.text = self.text + message
        sys.__stdout__.write(message)
        sys.__stdout__.flush()

    def flush(self):
        pass

    def cprint(self, *args):
        message = " ".join(map(str, args))
        Clock.schedule_once(lambda dt: self._clock(message=message), 0)

    def _clock(self, message):
        if message is not None:
            self.write(message + "\n")
