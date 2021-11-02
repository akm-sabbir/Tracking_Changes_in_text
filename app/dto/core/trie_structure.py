from collections import defaultdict


class Trie(object):
    def __init__(self):
        self.current_elem = defaultdict()
        self.isWord = False
        self.isLeaf = True
        self.isRoot = False
        self.word = None
        self.unicodePoint = None
        return

    def __call__(self):
        return