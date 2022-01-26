import spacy

from app.service.icd10_smoking_pattern_service import ICD10SmokingPatternDetection
from app.util.smoker_information_parser import SmokerInfoParser


class ICD10SmokingPatternDecisionImpl(ICD10SmokingPatternDetection):
    smoker_parser: SmokerInfoParser = SmokerInfoParser()
    bag_of_words = set(["smokers", "smoker", "smoke", "smoking", "smoked", "tobacco", "tobaco","cigarette",
                        "cigarettes",
                        "light smoker",
                        "light tobacco smoker",
                        "heavy smoker",
                        "heavy tobacco smoker",
                        "chain smoker"])
    nlp_algo: spacy.Language

    def __init__(self, nlp=None):
        self.nlp_algo = nlp

    def get_smoking_pattern_decision(self, text: str) -> bool:
        text = text.replace("(", " ")
        text = text.replace(")", " ")
        text = text.replace("/", " ")
        line = self.smoker_parser.get_parsed_info(text=text)
        if line != None:
            doc = self.nlp_algo(line.lower())
            smoker = False
            for word in doc.ents:
                if str(word) in self.bag_of_words:
                    smoker = False if word._.negex is True else True
                    break
            return smoker
        return False
