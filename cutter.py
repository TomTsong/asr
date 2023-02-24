from pydub import AudioSegment

import logging
import math

logger = logging.getLogger()


class Cutter:
    def __init__(self, filepath, duration=30):
        self.filepath = filepath
        self.duration = duration
        self.audio = AudioSegment.from_file(filepath)
        self.total_duration = len(self.audio)
        self.segments = math.ceil(len(self.audio) / duration / 1000)
        self.path, self.ext = filepath.rsplit(".", 1)
        self.seek = 0

    def get_piece_filename(self, index):
        return f"{self.path}-{index}.{self.ext}"

    def cut(self):
        logger.info(f"{self.filepath}: total -> {self.total_duration}, segments -> {self.segments}")
        start = 0
        for seg in range(self.segments):
            piece = self.audio[start: start + self.duration * 1000]
            f = self.get_piece_filename(seg)
            piece.export(f)
            start += 30 * 1000

        return

    def pieces(self):
        logger.info(f"{self.filepath}: total -> {self.total_duration}, segments -> {self.segments}")
        start = 0
        for seg in range(self.segments):
            piece = self.audio[start: start + self.duration * 1000]
            f = self.get_piece_filename(seg)
            piece.export(f)
            start += 30 * 1000
            yield file



if __name__ == "__main__":
    file = "./download/20230221_155642.m4a"
    cutter = Cutter(file)
    cutter.cut()
