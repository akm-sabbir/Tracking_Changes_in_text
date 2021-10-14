class Paragraph:

    def __init__(self, text, start_index, end_index):
        self.text = text
        self.start_index = start_index
        self.end_index = end_index

    text: str
    start_index: int
    end_index: int
