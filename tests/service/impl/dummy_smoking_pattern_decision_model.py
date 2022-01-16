from typing import List

import spacy


class Negation:
    negex: bool

    def __init__(self, negex: bool):
        self.negex = negex


class Doc:
    _: Negation

    def __init__(self, word, neg: Negation):
        self.word = word
        self._ = neg

    def __str__(self):
        return self.word


class Language:
    ents: Doc = []

    def __init__(self):
        pass


class DummySciSpacyModel(object):
    ents: List[Doc] = []

    def return_mock_docs(self):
        return self.ents

    def append_documents(self, doc: Doc):
        self.ents.append(doc)

    def nlp_process(self, text):
        words = text.split(' ')
        for each in words:
            self.ents.append(Doc(each, Negation(True)))
        return self

    def get_language(self):
        return Language()
