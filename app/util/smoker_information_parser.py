import codecs
import os
from collections import Counter


class SmokerInfoParser():

    bag_of_words = set(["patient", "currently", "smoke?"])
    counter = Counter()

    def get_parsed_info(self, text="Was the patient queried about smoking behavior? Yes No \n"
                                   "Does the patient currently smoke? Smoking: Patient has never smoked - (1/7/2020).\n"
                                   "Has pt had any testing done since last visit? Yes No bone scan last year at family "
                                   "care, colodone last year by elglo\n"
                                   "Has pt seen any specialist since last visit? Yes No\n"
                                   "Has pt been to the Hospital or ER since last visit?\n"):
        if text is None:
            raise ValueError("data is empty and null unable to process")

        self.counter.clear()
        text = text.split("\n")
        for each_line in text:
            for elem in each_line.lower().split():
                if elem in self.bag_of_words:
                    self.counter[elem] += 1
            if len(self.counter.keys()) == len(self.bag_of_words):
                sentences = each_line.lower().split("?")
                if len(sentences) > 1:
                    if sentences[1].strip().find("smoking:") == 0:
                        sentences[1] = sentences[1][9:]
                    return sentences[1].strip()
        return None