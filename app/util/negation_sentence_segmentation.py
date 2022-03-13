from spacy.language import Language


@Language.component('set_custom_boundaries')
def set_custom_boundaries(doc):
    for token in doc[:-1]:
        if token.text == "," or token.text == "(" or token.text == ".":
            doc[token.i + 1].is_sent_start = True
        elif token.text == ")":
            doc[token.i + 1].is_sent_start = False
    return doc
