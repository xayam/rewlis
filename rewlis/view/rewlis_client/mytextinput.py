from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.uix.textinput import TextInput

from rewlis.entity import *


class MyTextInput(TextInput):

    def __init__(self, model, **kwargs):
        self.model = model
        self.controller = self.model.controller
        super().__init__(
            size_hint=(1, None),
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
        self.is_focusable = False

    def on_text(self, instance=None, __=None):
        self.model.log.debug("Enter to function 'MyTextInput.on_text()'")
        if self.model.current_select in self.model.opt[POSITIONS]:
            if self.model.opt[POSITIONS][self.model.current_select][AUDIO] == EN:
                if instance == self.controller.table_label_left:
                    self._on_text(mp3=self.model.conf.ENG_MP3)
            else:
                if instance == self.controller.table_label_right:
                    self._on_text(mp3=self.model.conf.RUS_MP3)
        self.resize()

    def resize(self):
        self.model.log.debug("Enter to function 'MyTextInput.resize()'")
        self.height = (len(self._lines) + 1) * (self.line_height + self.line_spacing)
        height = Window.height - self.controller.container.tab_height - 6
        self.height = max([self.height, height])
        height = self.controller.table_navigator.children[0].height
        self.font_size = str(int(float(self.model.opt[FONTSIZESCALE]) * height / 3)) + "px"

    def _on_text(self, mp3):
        self.model.log.debug("Enter to function 'MyTextInput._on_text()'")
        if self.model.sound is None:
            self.model.log.debug("WARNING: self.model.sound is None")
        else:
            self.model.sound.stop()
            if self.model.clock_action is None:
                self.model.log.debug("WARNING: self.model.clock_action is None")
            else:
                self.model.clock_action.cancel()
        load = self.model.current_select + mp3
        self.model.log.debug("MySound().load_seek")
        self.model.sound = SoundLoader.load(load).load_seek(
            position=self.model.get_sound_pos(),
            atempo=self.model.opt[SPEED])
        self.model.pts_action = 0
        self.model.count_action = 0
        self.model.log.debug("Create Clock.schedule_interval(self.controller.action.clock_action_time, 0.5)")
        self.model.clock_action = Clock.schedule_interval(self.controller.action.clock_action_time, 0.5)
