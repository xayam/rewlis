import sox
import os


class AudioClass:
    def __init__(self, cprint, audio_list, output, language):
        self.cprint = cprint
        self.MP3 = f"{output}/{language}.mp3"
        self.WAV = f"{output}/{language}.wav"
        self.FLAC = f"{output}/{language}.flac"
        self.audio_list = audio_list
        if self.audio_list:
            self.create_mp3()
            self.create_wav()
            self.create_flac()
        else:
            self.cprint("Error: mp3 files not found")
            raise Exception("Error: mp3 files not found")

    def create_mp3(self):
        if os.path.exists(self.MP3):
            return
        # self.cprint("Create mp3...")
        cbn = sox.Combiner()
        cbn.convert(samplerate=16000, n_channels=1)
        cbn.build(self.audio_list, self.MP3, 'concatenate')

    def create_wav(self):
        if os.path.exists(self.WAV):
            return
        self.cprint("Converting mp3 to wav...")
        cbn = sox.Transformer()
        cbn.convert(samplerate=16000, n_channels=1)
        cbn.build(self.MP3, self.WAV)

    def create_flac(self):
        if os.path.exists(self.FLAC):
            return
        self.cprint("Converting mp3 to flac...")
        cbn = sox.Transformer()
        cbn.convert(samplerate=16000, n_channels=1)
        cbn.build(self.MP3, self.FLAC)
