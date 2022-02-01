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
    ents: List[Doc]

    def __init__(self, doc):
        self.ents = doc


class DummySciSpacyModel(object):

    polarity: bool = False

    def return_mock_docs(self):
        return self.ents

    def append_documents(self, doc: Doc):
        self.ents.append(doc)

    def nlp_process(self, text):
        ents: List[Doc] = []
        words = text.split(' ')
        for each in words:
            ents.append(Doc(each, Negation(self.polarity)))
        return Language(doc=ents)

    def set_doc_entity_polarity(self, polarity=False):
        self.polarity = polarity

    def get_language(self):
        return Language(Doc("", -1))
