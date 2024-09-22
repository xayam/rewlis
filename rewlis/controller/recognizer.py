import os
import wave
from vosk import Model, KaldiRecognizer


class RecognizerClass:
    def __init__(self, controller, model_path, output, language, config):
        self.controller = controller
        self.language = language
        if self.language == "rus":
            self.MAPJSON = f"{output}/{config.RUS_MAP}"
            self.WAV = f"{output}/{config.RUS_WAV}"
        else:
            self.MAPJSON = f"{output}/{config.ENG_MAP}"
            self.WAV = f"{output}/{config.ENG_WAV}"
        self.MODEL_PATH = model_path

    def create_map(self):
        if os.path.exists(self.MAPJSON):
            self.controller.cprint("Find file self.MAPJSON")
            return True
        wf = wave.open(self.WAV, "rb")
        model = Model(self.MODEL_PATH)
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)
        ss = '{\n"fragments": [\n'
        while True:
            dat = wf.readframes(4000)
            if len(dat) == 0:
                break
            if rec.AcceptWaveform(dat):
                sss = rec.Result()
                ss += sss + ",\n"
                self.controller.cprint(sss)
        ss += rec.FinalResult() + "]}"
        with open(self.MAPJSON, mode="w", encoding="UTF-8") as ff:
            ff.write(ss)
        self.controller.cprint("Create file self.MAPJSON")
        return True
