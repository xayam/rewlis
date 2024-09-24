import json
import os
import sys
import wave
from multiprocessing.dummy import Pool
from vosk import Model, KaldiRecognizer


class RecognizerClass:
    def __init__(self, cprint, model_path, output, language, config):
        self.chunk = None
        self.cprint = cprint
        self.language = language
        if self.language == "rus":
            self.MAPJSON = f"{output}/{config.RUS_MAP}"
        else:
            self.MAPJSON = f"{output}/{config.ENG_MAP}"
        self.WAV = [i for i in os.listdir(f"{output}/wav{self.language}")
                    if i.endswith(".wav")]
        self.MODEL_PATH = model_path
        self.create_map()

    def create_map(self):
        if os.path.exists(self.MAPJSON):
            self.cprint(f"Find file '{self.MAPJSON}'")
            return True
        n = 4
        p = Pool(n)
        results = p.map(self.recognize, self.WAV)
        self.cprint(results)
        sys.exit()
        # result = '{\n"fragments": [\n'
        # result += ",\n"
        # result += "]}"
        # with open(self.MAPJSON, mode="w", encoding="UTF-8") as ff:
        #     ff.write(result)
        # self.cprint(f"Create file '{self.MAPJSON}'")
        return True

    def recognize(self, wav):
        wf = wave.open(wav, "rb")
        model = Model(self.MODEL_PATH)
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)
        result = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                buffer = rec.Result()
                result.append(buffer)
                self.cprint(buffer)
        result.append(rec.FinalResult())
        return result
