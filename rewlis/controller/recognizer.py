import json
import os
import wave
import mutagen.mp3

import concurrent.futures
from vosk import Model, KaldiRecognizer


class RecognizerClass:
    def __init__(self, cprint, model_path, output, language, config, mp3_list):
        self.chunk = None
        self.cprint = cprint
        self.language = language
        self.audio_list = mp3_list
        self.cprint(mp3_list)
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
        self.cprint("Start recognize...")
        results = []
        futures = []
        sizes1 = [mutagen.mp3.MP3(mp3_list[2]).info.length
                  for mp3_list in self.audio_list]
        shift = 0
        sizes = []
        for s in sizes1:
            sizes.append(s + shift)
            shift += s
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for i in range(len(self.WAV)):
                futures.append(executor.submit(
                    self.recognize, self.WAV[i], sizes[i]))
            executor.shutdown()
            for future in futures:
                results.append(future.result())
        buffer = "  "
        self.cprint("point 0")
        for result in results:
            self.cprint("point 1")
            buffer += ",\n".join(result)
        self.cprint("point 2")
        result = '{\n"fragments": [\n'
        result += buffer[:-2]
        result += "]}"
        with open(self.MAPJSON, mode="w", encoding="UTF-8") as ff:
            ff.write(result)
        self.cprint(f"Created file '{self.MAPJSON}'")
        return True

    def recognize(self, wav, size):
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
                buffer = self.update_buffer(buffer=rec.Result(), size=size)
                result.append(buffer)
                self.cprint(buffer)
        result.append(
            self.update_buffer(buffer=rec.FinalResult(), size=size)
        )
        return result

    @staticmethod
    def update_buffer(buffer, size):
        r = json.loads(buffer)
        try:
            for i in range(len(r["result"])):
                r["result"][i]["end"] += size
                r["result"][i]["start"] += size
        except KeyError:
            pass
        buffer = json.dumps(buffer).encode(errors="ignore").decode('unicode-escape')
        buffer = buffer[1:] if buffer[0] == '"' else buffer
        buffer = buffer[:-1] if buffer[-1] == '"' else buffer
        return buffer
