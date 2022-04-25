from app.service.icd10_text_token_span_gen_service import ICD10TextTokenAndSpanGeneration
from nltk import TreebankWordTokenizer
import string
from app.dto.core.service.Tokens import TokenInfo
from typing import List

""" this class we designed to break down the text into smallest tokens and
retrieve the span of each token in original text so that we can accurately shows
 span of text segment for which we have retrieved icd10 code in front end side"""


class ICD10TextAndSpanGenerationServiceImpl(ICD10TextTokenAndSpanGeneration):

    def __init__(self):
        self.__tokenizer = TreebankWordTokenizer()

    def _tokenize_with_span(self, text):
        ts = [TokenInfo(token=text[start:end], start_of_span=start, end_of_span=end)
              for start, end in self.__tokenizer.span_tokenize(text)]
        return ts

    """following function generate tokens and actual span for a given text content"""
    def process_each_token(self, spanned_info: List[TokenInfo]) -> list:
        new_spanned_info = []
        for each_span in spanned_info:
            each_span.token, each_span.end_of_span, new_comp = (each_span.token[0:-1], (each_span.end_of_span - 1),
                                                                each_span.token[-1:]) if len(each_span.token) > 1 and \
                                            each_span.token[-1] in string.punctuation \
                                            else (each_span.token, each_span.end_of_span, None)
            new_spanned_info.append(each_span)
            if new_comp is not None:
                new_span = TokenInfo(token=new_comp, start_of_span=each_span.end_of_span, end_of_span=each_span.end_of_span + len(new_comp))
                new_spanned_info.append(new_span)

        return new_spanned_info

    """Following function is used to remove any empty token"""
    def remove_empty_string(self, spanned_info_list) -> list:
        return list(filter(lambda x: len(x.token) > 0, spanned_info_list))

    """we expect following output [["token1", start index, end index], ["token2", start, end] ...]
    from the below funtion"""
    def get_token_with_span(self, text: str) -> List[TokenInfo]:
        tokenized_text = self._tokenize_with_span(text)
        tokenized_text = self.process_each_token(tokenized_text)
        tokenized_text = self.remove_empty_string(tokenized_text)
        return tokenized_text