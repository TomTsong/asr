import logging

import whisper


logger = logging.getLogger("recognizer")


class SpeechRecognizer:
    def __init__(self, model_name="base", device=None):
        self.model_name = model_name
        self.model = None
        self.device = device

    def load_model(self):
        self.model = whisper.load_model(self.model_name, device=self.device)

    def auto_recognize(self, filepath, language=None, **kwargs):
        if self.model is None:
            self.model = whisper.load_model(self.model_name)

        fp16 = None
        if str(self.model.device).startswith("cpu"):
            fp16 = False

        # no_speech_threshold=0.6
        result = self.model.transcribe(filepath, language=language, verbose=True, fp16=fp16)
        return result


class MyRecognizer:
    def __init__(self, model):
        self.model = model

    def auto_recognize(self, filepath, language=None, **kwargs):
        fp16 = None
        if str(self.model.device).startswith("cpu"):
            fp16 = False

        result = self.model.transcribe(filepath, language=language, verbose=True, fp16=fp16)
        return result


if __name__ == "__main__":
    sr = SpeechRecognizer(model_name="large")
    # file = "./download/20230221_155642.m4a"
    # file = "./download/20230221_114814.m4a"
    # file = "./download/output.aac"
    file = "./download/20230221_155642-3.m4a"
    res = sr.auto_recognize(file)
