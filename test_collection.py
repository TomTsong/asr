
class A:
    def __init__(self, filepath):
        self.filepath = filepath
        self.total_duration = 1000
        self.segments = 20

    def get_piece_filename(self, index):
        return f"{index}.aac"

    def pieces(self):
        print(f"{self.filepath}: total -> {self.total_duration}, segments -> {self.segments}")
        start = 0
        for seg in range(self.segments):
            f = self.get_piece_filename(seg)
            print(f)
            start += 30 * 1000
            yield f


if __name__ == "__main__":
    a = A("aaa.aac")
    for piece in a.pieces():
        print(piece)
        