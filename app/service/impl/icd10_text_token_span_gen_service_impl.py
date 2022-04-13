from app.service.icd10_text_token_span_gen_service import ICD10TextTokenAndSpanGeneration
from app.dto.core.util import Span
from nltk import TreebankWordTokenizer
import re
import string


class ICD10TextAndSpanGenerationServiceImpl(ICD10TextTokenAndSpanGeneration):

    def __init__(self):
        self.__tokenizer = TreebankWordTokenizer()

    def _tokenize_with_span(self, text):
        ts = [[text[start:end], start, end] for start, end in self.__tokenizer.span_tokenize(text)]
        return ts

    def process_each_token(self, spanned_info) -> list:
        new_spanned_info = []
        for each_span in spanned_info:
            each_span[0], each_span[2], new_comp = (each_span[0][0:-1], (each_span[2] - 1), each_span[0][-1:]) \
                                            if len(each_span[0]) > 1 and \
                                            each_span[0][-1] in string.punctuation else (each_span[0], each_span[2], None)
            new_spanned_info.append(each_span)
            if new_comp is not None:
                new_span = []
                new_span.append(new_comp)
                new_span.append(each_span[2])
                new_span.append(each_span[2] + len(new_comp))
                new_spanned_info.append(new_span)

        return new_spanned_info

    def remove_empty_string(self, spanned_info_list) -> list:
        return list(filter(lambda x: len(x[0]) > 0, spanned_info_list))

    def get_token_with_span(self, text: str) -> list:
        tokenized_text = self._tokenize_with_span(text)
        tokenized_text = self.process_each_token(tokenized_text)
        tokenized_text = self.remove_empty_string(tokenized_text)
        return tokenized_text