from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.core.window import Window

from rewlis.entity import *


class Options(TabbedPanelItem):
    def __init__(self, model):
        self.model = model
        self.controller = self.model.controller

        TabbedPanelItem.__init__(self,
                                 background_normal=self.model.conf.ICON_OPTIONS,
                                 background_down=self.model.conf.ICON_OPTIONS_PRESSED)
        # height1 = self.controller.table_navigator.children[0].height
        height1 = Window.width // 15
        height2 = str(height1 - 10) + "px"
        width1 = str(2 * height1) + "px"
        height1 = str(height1) + "px"
        self.options_fontsize_layout = BoxLayout(
            size_hint=(1, None),
            height=height1,
            pos_hint={"top": 0.60, "x": 0},
            # padding=(10, 20)
        )
        self.options_fontsize_label = Label(text="FontSize scale",
                                            font_size=height2)
        self.controller.options_fontsize_scale = \
            Label(text=self.model.opt[FONTSIZESCALE],
                  size_hint=(None, 1),
                  width=width1,
                  font_size=height2)
        self.options_fontsize_down = Button(
            size_hint=(None, 1),
            width=height1,
            background_normal=self.model.conf.ICON_DOWN,
            background_down=self.model.conf.ICON_DOWN_PRESSED,
            on_release=self.options_fontsize_down_click)
        self.options_fontsize_up = Button(
            size_hint=(None, 1),
            width=height1,
            background_normal=self.model.conf.ICON_UP,
            background_down=self.model.conf.ICON_UP_PRESSED,
            on_release=self.options_fontsize_up_click)

        self.options_speed_layout = BoxLayout(
            size_hint=(1, None),
            height=height1,
            pos_hint={"top": 0.40, "x": 0},
            # padding=(10, 20)
        )
        self.options_speed_tempo = Label(text="Speed tempo",
                                         font_size=height2)
        self.controller.options_speed_tempo = \
            Label(text=self.model.opt[SPEED],
                  size_hint=(None, 1),
                  width=width1,
                  font_size=height2)
        self.options_speed_down = Button(
            size_hint=(None, 1),
            width=height1,
            background_normal=self.model.conf.ICON_DOWN,
            background_down=self.model.conf.ICON_DOWN_PRESSED,
            on_release=self.options_speed_down_click)
        self.options_speed_up = Button(
            size_hint=(None, 1),
            width=height1,
            background_normal=self.model.conf.ICON_UP,
            background_down=self.model.conf.ICON_UP_PRESSED,
            on_release=self.options_speed_up_click)
        self.options_speed_layout.add_widget(self.options_speed_tempo)
        self.options_speed_layout.add_widget(self.options_speed_down)
        self.options_speed_layout.add_widget(self.options_speed_up)
        self.options_speed_layout.add_widget(self.controller.options_speed_tempo)

        self.options_fontsize_layout.add_widget(self.options_fontsize_label)
        self.options_fontsize_layout.add_widget(self.options_fontsize_down)
        self.options_fontsize_layout.add_widget(self.options_fontsize_up)
        self.options_fontsize_layout.add_widget(self.controller.options_fontsize_scale)
        self.item_options_layout = RelativeLayout()
        self.item_options_layout.add_widget(self.options_fontsize_layout)
        self.item_options_layout.add_widget(self.options_speed_layout)
        self.add_widget(self.item_options_layout)

    def options_fontsize_down_click(self, _=None):
        self.controller.player.pause_button_click()
        value = float(self.controller.options_fontsize_scale.text)
        value = 0.1 if value <= 0.1 else value - 0.1
        self.controller.options_fontsize_scale.text = "%.1f" % value
        self.model.opt[FONTSIZESCALE] = self.controller.options_fontsize_scale.text
        self.model.conf.save_options()
        self.controller.table_label_left.resize()
        self.controller.table_label_right.resize()

    def options_fontsize_up_click(self, _=None):
        self.controller.player.pause_button_click()
        value = float(self.controller.options_fontsize_scale.text)
        value = 9.9 if value >= 9.9 else value + 0.1
        self.controller.options_fontsize_scale.text = "%.1f" % value
        self.model.opt[FONTSIZESCALE] = self.controller.options_fontsize_scale.text
        self.model.conf.save_options()
        self.controller.table_label_left.resize()
        self.controller.table_label_right.resize()

    def options_speed_down_click(self, _=None):
        if self.model.target == TARGET_ANDROID:
            return
        self.controller.player.pause_button_click()
        value = float(self.controller.options_speed_tempo.text)
        value = 0.5 if value <= 0.5 else value - 0.1
        self.controller.options_speed_tempo.text = "%.1f" % value
        self.model.opt[SPEED] = self.controller.options_speed_tempo.text
        self.model.conf.save_options()

    def options_speed_up_click(self, _=None):
        if self.model.target == TARGET_ANDROID:
            return
        self.controller.player.pause_button_click()
        value = float(self.controller.options_speed_tempo.text)
        value = 9.9 if value >= 9.9 else value + 0.1
        self.controller.options_speed_tempo.text = "%.1f" % value
        self.model.opt[SPEED] = self.controller.options_speed_tempo.text
        self.model.conf.save_options()
