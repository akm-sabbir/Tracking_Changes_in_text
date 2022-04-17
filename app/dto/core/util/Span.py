
class Span:
    start: int = 0
    end: int = 0
    offset: int = 0

    def __init__(self, start=0, end=0, offset=0):
        self.start = start
        self.end = end
        self.offset = offset