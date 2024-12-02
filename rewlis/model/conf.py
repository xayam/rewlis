import json
import os

from rewlis.entity import *


class Conf:

    NAME = "Rewlis"

    OPTIONS = "options.json"
    CONFIG = "config.sh"
    FOLDER_CREATE = "create"
    FOLDER_PUBLIC = "data"
    LICENSE = "LICENSE"
    CASES_HTML = os.getcwd() + "/cases.html"
    README_MD = os.getcwd() + "/README.md"
    FAQ_HTML = os.getcwd() + "/faq.html"
    DONATE = "https://yoomoney.ru/to/410014160363421"
    ICON_ICO = "data/resources/img/icon.ico"
    ICON_PNG = "data/resources/img/icon.png"

    GIT_REWLIS = "https://hub.mos.ru/xayam.ru/rewlis"
    UPDATE_URL = \
        "https://hub.mos.ru/xayam.ru/rewlis/" + \
        ""
    # Copy here
    # UPDATE_URL = "https://cloud.mail.ru/public/rdBB/KHvCjQdaT/Android/"
    LIST_FILE = "list.zip"
    LIST_URL = UPDATE_URL + LIST_FILE
    CHAT_REWLIS = "https://t.me/rewlis"
    TELEGRAM_REWLIS = "@rewlis"
    EMAIL = "xayam@yandex.ru"

    DISABLE_MARKER = "data/resources/img/marker.png"
    # Icon paths
    ICON_CATALOG = "data/resources/img/catalog.png"
    ICON_CATALOG_PRESSED = "data/resources/img/catalog_pressed.png"
    ICON_TABLE = "data/resources/img/table.png"
    ICON_TABLE_PRESSED = "data/resources/img/table_pressed.png"
    ICON_OPTIONS = "data/resources/img/options.png"
    ICON_OPTIONS_PRESSED = "data/resources/img/options_pressed.png"
    ICON_PREV = "data/resources/img/prev.png"
    ICON_PREV_PRESSED = "data/resources/img/prev_pressed.png"
    ICON_PLAY = "data/resources/img/play.png"
    ICON_PLAY_PRESSED = "data/resources/img/play_pressed.png"
    ICON_PAUSE = "data/resources/img/pause.png"
    ICON_PAUSE_PRESSED = "data/resources/img/pause_pressed.png"
    ICON_STOP = "data/resources/img/stop.png"
    ICON_STOP_PRESSED = "data/resources/img/stop_pressed.png"
    ICON_NEXT = "data/resources/img/next.png"
    ICON_NEXT_PRESSED = "data/resources/img/next_pressed.png"
    ICON_DOWN = "data/resources/img/down.png"
    ICON_DOWN_PRESSED = "data/resources/img/down_pressed.png"
    ICON_UP = "data/resources/img/up.png"
    ICON_UP_PRESSED = "data/resources/img/up_pressed.png"

    def __init__(self, model):
        self.model = model
        self.controller = self.model.controller
        self.app = self.model.app

        self.locale = None
        self.load_options()
        self.set_locale(self.model.opt[LOCALE])

    def set_locale(self, locale):
        self.locale = locale

    def load_options(self):
        if os.path.exists(self.OPTIONS):
            with open(self.OPTIONS, mode="r") as opt:
                self.model.opt = json.load(opt)
        else:
            self.save_options()

    def save_options(self):
        if self.controller is None:
            return
        json_string = json.dumps(self.model.opt)
        with open(self.OPTIONS, mode="w") as opt:
            opt.write(json_string)
