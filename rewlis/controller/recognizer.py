import json
import os
import sys
import wave
import mutagen.mp3

import concurrent.futures
from vosk import Model, KaldiRecognizer


class RecognizerClass:
    def __init__(self, cprint, model_path, output, language, config, mp3):
        self.chunk = None
        self.cprint = cprint
        self.language = language
        self.audio_list = mp3
        if self.language == "rus":
            self.MAPJSON = f"{output}/{config.RUS_MAP}"
        else:
            self.MAPJSON = f"{output}/{config.ENG_MAP}"
        self.WAV = [f"{output}/wav{self.language}/{i}"
                    for i in os.listdir(f"{output}/wav{self.language}")
                    if i.endswith(".wav")]
        self.MODEL_PATH = model_path
        self.create_map()

    def create_map(self):
        if os.path.exists(self.MAPJSON):
            self.cprint(f"Find file '{self.MAPJSON}'")
            return True
        results = []
        futures = []
        sizes = [mutagen.mp3.MP3(mp3[2]).info.length for mp3 in self.audio_list]
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for args in self.WAV:
                futures.append(executor.submit(self.recognize, args))
            executor.shutdown()
            for future in futures:
                results.append(future.result())
        buffer = ""
        index = 0
        sizes_index = 0
        for result in results:
            for res in result:
                r = json.loads(res)
                if r.__contains__("result"):
                    for i in range(len(r["result"])):
                        r["result"][i]["end"] += sizes_index
                        r["result"][i]["start"] += sizes_index
                buffer += json.dumps(r) + ",\n"
            sizes_index += sizes[index]
            index += 1
        result = '{\n"fragments": [\n'
        result += buffer
        result += "]}"
        with open(self.MAPJSON, mode="w", encoding="UTF-8") as ff:
            ff.write(result)
        self.cprint(f"Created file '{self.MAPJSON}'")
        return True

    def recognize(self, wav):
        wf = wave.open(wav, "rb")
        self.cprint("Loading recognize model...")
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
