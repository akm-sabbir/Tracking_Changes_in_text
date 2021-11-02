from collections import defaultdict


class Trie(object):
    is_word: bool

    def __init__(self):
        self.current_elem = defaultdict()
        self.is_word = False
        self.is_leaf = True
        self.is_root = False
        self.word = None
        self.unicodePoint = None
        return

    def __call__(self):
        return