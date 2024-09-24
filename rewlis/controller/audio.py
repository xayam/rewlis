import sox
import os


class AudioClass:
    def __init__(self, cprint, audio_list, output, language):
        self.cprint = cprint
        self.audio_list = audio_list
        self.language = language
        self.MP3 = f"{output}/{self.language}.mp3"
        self.WAV = [f"{output}/wav{self.language}/{i[1][-4:]}.wav"
                    for i in self.audio_list]
        self.FLAC = f"{output}/{self.language}.flac"
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
        self.cprint("Create mp3...")
        cbn = sox.Combiner()
        cbn.convert(samplerate=16000, n_channels=1)
        list_input = [f"{i[0]}/mp3{self.language}/{i[1]}"
                      for i in self.audio_list]
        cbn.build(list_input, self.MP3, 'concatenate')

    def create_wav(self):
        self.cprint("Converting mp3 to wav...")
        cbn = sox.Transformer()
        cbn.convert(samplerate=16000, n_channels=1)
        for i in range(self.audio_list):
            if os.path.exists(self.WAV[i]):
                continue
            cbn.build(self.MP3, self.WAV[i])

    def create_flac(self):
        if os.path.exists(self.FLAC):
            return
        self.cprint("Converting mp3 to flac...")
        cbn = sox.Transformer()
        cbn.convert(samplerate=16000, n_channels=1)
        cbn.build(self.MP3, self.FLAC)
