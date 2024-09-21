import os

from kivy.core.audio import SoundLoader
from kivy.core.audio.audio_ffpyplayer import SoundFFPy
from ffpyplayer.player import MediaPlayer
import mutagen.mp3

from rewlis.entity import *


class MySound(SoundFFPy):

    def __init__(self, **kwargs):
        super(MySound, self).__init__(**kwargs)
        self.model = None
        self.ffplayer = None
        self.has_stop = False

    def _get_length(self):
        return mutagen.mp3.MP3(self.source).info.length

    def load_seek(self, position, atempo):
        self._state = ''
        self.state = 'stop'
        self.quitted = False

        ff_opts = {
            'vn': True,  # video disable
            'sn': True,  # subtitle disable
            'ss': position,  # seek position
            # 'infbuf': True,
            # 'genpts': True,
            # 'fast': True,
            'ar': 16000,  # audio rate
            'ac': 1,  # count audio channels
        }
        if os.environ["TARGET_PLATFORM"] == TARGET_WINDOWS:
            ff_opts['af'] = "atempo=" + atempo  # audio speed tempo
        print(f"[MYDEBUG] Length mp3 is {self.length}")
        print(f"[MYDEBUG] Seek position ff_opts['ss'] is {position}")
        print(f"[MYDEBUG] Set self._ffplayer = MediaPlayer({self.source})")
        self._ffplayer = MediaPlayer(self.source,
                                     callback=self._player_callback,
                                     loglevel='debug',
                                     ff_opts=ff_opts)
        self._state = 'playing'
        self.state = 'play'
        self.ffplayer = self._ffplayer
        print(f"[MYDEBUG] Seek ffplayer")
        self.ffplayer.seek(pts=position,
                           seek_by_bytes=False,
                           relative=False,
                           accurate=False)
        print(f"[MYDEBUG] Exit from function 'load_seek()'")
        return self


SoundLoader._classes = []
SoundLoader.register(MySound)
