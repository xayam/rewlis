import sys

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
            background_color=(0., 0., 0., 1.),
            foreground_color=(1., 1., 1., 1.),
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
