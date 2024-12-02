from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanelItem

from rewlis.view.rewlis_client.mytextinput import MyTextInput


class Table(TabbedPanelItem):
    def __init__(self, model):
        self.model = model
        self.controller = self.model.controller

        TabbedPanelItem.__init__(self,
                                 background_normal=self.model.conf.ICON_TABLE,
                                 background_down=self.model.conf.ICON_TABLE_PRESSED)
        self.table_gridlayout = GridLayout(cols=3, padding=(6, 6), spacing=3)
        self.controller.table_navigator = BoxLayout(orientation="vertical",
                                                    size_hint=(1, 0.3))
        self.table_prev = Button(background_normal=self.model.conf.ICON_PREV,
                                 background_down=self.model.conf.ICON_PREV_PRESSED,
                                 on_release=self.controller.player.prev_button_click)
        self.controller.table_navigator.add_widget(self.table_prev)
        self.table_play = Button(background_normal=self.model.conf.ICON_PLAY,
                                 background_down=self.model.conf.ICON_PLAY_PRESSED,
                                 on_release=self.controller.player.play_button_click)
        self.controller.table_navigator.add_widget(self.table_play)
        self.table_pause = Button(
            background_normal=self.model.conf.ICON_PAUSE,
            background_down=self.model.conf.ICON_PAUSE_PRESSED,
            on_release=self.controller.player.pause_button_click)
        self.controller.table_navigator.add_widget(self.table_pause)
        self.table_stop = Button(background_normal=self.model.conf.ICON_STOP,
                                 background_down=self.model.conf.ICON_STOP_PRESSED,
                                 on_release=self.controller.player.stop_button_click)
        self.controller.table_navigator.add_widget(self.table_stop)
        self.table_next = Button(background_normal=self.model.conf.ICON_NEXT,
                                 background_down=self.model.conf.ICON_NEXT_PRESSED,
                                 on_release=self.controller.player.next_button_click)
        self.controller.table_navigator.add_widget(self.table_next)
        self.table_gridlayout.add_widget(self.controller.table_navigator)
        self.controller.table_book_left = ScrollView(do_scroll_x=False,
                                                     do_scroll_y=True,
                                                     bar_width=15)
        self.controller.table_label_left = MyTextInput(
            model=self.model,
            text="Select a book in the 'Catalog' section")
        self.controller.table_label_left.bind(
            on_touch_down=self.controller.action.touch_down_click)
        self.controller.table_label_left.bind(
            on_double_tap=self.controller.action.double_tap)
        self.controller.table_label_left.height = \
            max([self.controller.table_label_left.minimum_height,
                 self.controller.table_book_left.height])
        self.controller.table_book_left.add_widget(self.controller.table_label_left)
        self.table_gridlayout.add_widget(self.controller.table_book_left)
        self.controller.table_book_right = ScrollView(do_scroll_x=False,
                                                      do_scroll_y=True,
                                                      bar_width=15)
        self.controller.table_label_right = MyTextInput(
            model=self.model,
            text="Выберите книгу в разделе 'Catalog'")
        self.controller.table_label_right.bind(
            on_touch_down=self.controller.action.touch_down_click)
        self.controller.table_label_right.bind(
            on_double_tap=self.controller.action.double_tap)
        self.controller.table_label_right.height = \
            max([self.controller.table_label_right.minimum_height,
                self.controller.table_book_right.height])
        self.controller.table_book_right.add_widget(
            self.controller.table_label_right)
        self.table_gridlayout.add_widget(self.controller.table_book_right)
        self.add_widget(self.table_gridlayout)
