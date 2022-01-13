import codecs
import os
from collections import Counter
import logging


class SmokerInfoParser():

    __bag_of_words = set(["patient", "currently", "smoke?"])
    __counter = Counter()
    __logger = logging.getLogger(__name__)

    def get_parsed_info(self, text):
        if text is None or len(text) == 0:
            self.__logger.error("data is empty and null unable to process")
            raise ValueError("data is empty and null unable to process")

        self.__counter.clear()
        text = text.split("\n")
        for each_line in text:
            for elem in each_line.lower().split():
                if elem in self.__bag_of_words:
                    self.__counter[elem] += 1
            if len(self.__counter.keys()) == len(self.__bag_of_words):
                sentences = each_line.lower().split("?")
                if len(sentences) > 1:
                    if sentences[1].strip().find("smoking:") == 0:
                        sentences[1] = sentences[1][9:]
                    return sentences[1].strip()
        return None