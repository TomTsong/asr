import logging
import os

import torch.cuda
import whisper

import config

logger = logging.getLogger("recognizer")


class SpeechRecognizer:
    def __init__(self, model_name="base"):
        self.model_name = model_name
        self.model = None

    def auto_recognize(self, filepath, language=None, **kwargs):
        if self.model is None:
            self.model = whisper.load_model(self.model_name)

        result = self.model.transcribe(filepath, language=language, verbose=True)
        return result


if __name__ == "__main__":
    import pandas as pd
    sr = SpeechRecognizer(model_name="large")
    # file = "./download/20230221_155642.m4a"
    # file = "./download/20230221_114814.m4a"
    # file = "./download/output.aac"
    file = "./download/20230221_155642-3.m4a"
    res = sr.auto_recognize(file)
    # df = pd.DataFrame(res["segments"])
    # print(df[["id", "seek", "start", "end", "text"]])
