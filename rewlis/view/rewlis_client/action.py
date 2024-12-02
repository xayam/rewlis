from kivy.clock import Clock
from kivy.core.audio import SoundLoader

from rewlis.entity import *


class Action:

    def __init__(self, model):
        self.model = model
        self.controller = self.model.controller
        self.app = self.model.app

    def touch_down_click(self, instance, event):
        self.model.log.debug("Enter to function 'touch_up_click()'")
        pos = instance.cursor_index(instance.get_cursor_from_xy(*event.pos))
        if self.model.touch_pos == pos:
            return True
        self.model.touch_pos = pos
        if self.model.clock_action is not None:
            self.model.clock_action.cancel()
        self.model.log.debug(f"Touch pos={pos}")
        if self.model.current_select in self.model.opt[POSITIONS]:
            if self.model.sound.has_stop:
                self.controller.player.play_button_click()
                return True
            if instance == self.controller.table_label_left:
                sync = self.model.syncs[self.model.current_select].book1.sync
                chunk = self.model.syncs[self.model.current_select].chunks1
            else:
                sync = self.model.syncs[self.model.current_select].book2.sync
                chunk = self.model.syncs[self.model.current_select].chunks2

            for p in range(self.model.chunk_current):
                pos += len(chunk[p])

            for i in range(len(sync)):
                if sync[i][POS_START] > pos:
                    self.model.log.debug("Stop and reload self.model.sound")
                    self.model.sound.stop()
                    self.model.opt[POSITIONS][
                        self.model.current_select][POSI] = \
                        sync[i][TIME_START]
                    self.model.set_sound_pos(sync[i][TIME_START])
                    if instance == self.controller.table_label_left:
                        self.model.opt[POSITIONS][
                            self.model.current_select][AUDIO] = EN
                        self.model.sound = SoundLoader.load(
                            self.model.current_select +
                            self.model.conf.ENG_MP3). \
                            load_seek(position=self.model.get_sound_pos(),
                                      atempo=self.model.opt[SPEED])
                    else:
                        self.model.opt[POSITIONS][
                            self.model.current_select][AUDIO] = RU
                        self.model.sound = SoundLoader.load(
                            self.model.current_select +
                            self.model.conf.RUS_MP3). \
                            load_seek(position=self.model.get_sound_pos(),
                                      atempo=self.model.opt[SPEED])
                    self.model.conf.save_options()
                    self.model.pts_action = 0
                    self.model.count_action = 0
                    self.model.log.debug(
                        f"Create Clock.schedule_interval(" +
                        "self.clock_action_time, timeout=0.5)")
                    self.model.clock_action = \
                        Clock.schedule_interval(
                            self.clock_action_time, 0.5)
                    return True
        else:
            self.model.touch_pos = 0
            self.controller.container.switch_to(self.controller.catalog)
            self.controller.catalog.on_resize(timeout_catalog=0)
        return True

    def double_tap(self, _=None, __=None, ___=None):
        self.model.log.debug("Fired function double_tap() for TextInput widget")

    def clock_action_time(self, _=None):
        self.model.log.debug("Enter to function 'clock_action_time()'")
        if self.model.opt[POSITIONS][self.model.current_select][AUDIO] == EN:
            text_area = self.controller.table_label_left
            book_area = self.controller.table_book_left
            text_area_other = self.controller.table_label_right
            book_area_other = self.controller.table_book_right
            chunk = self.model.syncs[self.model.current_select].chunks1
            chunk_other = self.model.syncs[self.model.current_select].chunks2
            sync = self.model.syncs[self.model.current_select].eng2rus
        else:
            text_area = self.controller.table_label_right
            book_area = self.controller.table_book_right
            text_area_other = self.controller.table_label_left
            book_area_other = self.controller.table_book_left
            chunk_other = self.model.syncs[self.model.current_select].chunks1
            chunk = self.model.syncs[self.model.current_select].chunks2
            sync = self.model.syncs[self.model.current_select].rus2eng
        if self.model.count_action == 0:
            pos = self.model.sound.ffplayer.get_pts()
            self.model.pts_action = pos
        else:
            pos = self.model.pts_action + \
                  (self.model.sound.ffplayer.get_pts() - self.model.pts_action) \
                  * float(self.model.opt[SPEED])
        self.model.count_action += 1
        self.model.log.debug(f"Getting self.model.sound.ffplayer.get_pts()={pos}")
        if self.model.sound.ffplayer.get_pts() + 1.0 >= \
                self.model.sound.ffplayer.get_metadata()['duration']:
            self.controller.player.stop_button_click()
            self.model.chunk_current = 0
            self.model.opt[POSITIONS][self.model.current_select][POSI] = "0.0"
            self.model.opt[POSITIONS][self.model.current_select][CHUNK] = 0
            self.model.conf.save_options()
            return

        try:
            position = 0
            for current in range(len(self.model.syncs[
                                         self.model.current_select].chunks1)):
                position += len(chunk[current])
                if position > sync[str(int(pos))][0]:
                    if current != self.model.chunk_current:
                        self.model.chunk_current = current
                        self.model.opt[POSITIONS][
                            self.model.current_select][CHUNK] = \
                            self.model.chunk_current
                        self.model.conf.save_options()
                        self.controller.table_label_left.text = \
                            self.model.syncs[
                                self.model.current_select].chunks1[
                                self.model.chunk_current]
                        self.controller.table_label_right.text = \
                            self.model.syncs[
                                self.model.current_select].chunks2[
                                self.model.chunk_current]
                        return
                    else:
                        break

            position = sync[str(int(pos))][0]
            for p in range(self.model.chunk_current):
                position -= len(chunk[p])
            self.model.log.debug(f"Position={position}")

            text_area.select_text(0, position)
            y1 = text_area.get_cursor_from_index(
                text_area.selection_to)[1]
            text_area.cursor = (0, y1)
            y = text_area.cursor_pos[1] - book_area.height + \
                y1 * (text_area.line_height + text_area.line_spacing)
            if y >= text_area.cursor_pos[1] - book_area.height // 2:
                y = text_area.cursor_pos[1] - book_area.height // 2
            if y < 0:
                y = 0
            book_area.scroll_y = book_area. \
                convert_distance_to_scroll(0, y)[1]

            position = sync[str(int(pos))][1]
            for p in range(self.model.chunk_current):
                position -= len(chunk_other[p])
            self.model.log.debug(f"Position_other={position}")

            text_area_other.select_text(0, position)
            y1 = text_area_other.get_cursor_from_index(
                text_area_other.selection_to)[1]
            text_area_other.cursor = (0, y1)
            y = text_area_other.cursor_pos[1] - book_area_other.height + \
                y1 * (text_area_other.line_height + text_area_other.line_spacing)
            if y >= text_area_other.cursor_pos[1] - book_area_other.height // 2:
                y = text_area_other.cursor_pos[1] - book_area_other.height // 2
            if y < 0:
                y = 0
            book_area_other.scroll_y = book_area_other. \
                convert_distance_to_scroll(0, y)[1]
        except Exception as e:
            self.model.log.debug(type(e).__name__ + ": " + e.__str__())
            return

        self.model.opt[POSITIONS][self.model.current_select][POSI] = \
            str(pos)
        self.model.opt[POSITIONS][self.model.current_select][CHUNK] = \
            self.model.chunk_current
        self.model.set_sound_pos(pos)
        self.model.conf.save_options()
