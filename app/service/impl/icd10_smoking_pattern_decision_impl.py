import spacy

from app.service.icd10_smoking_pattern_service import ICD10SmokingPatternDetection
from app.util.smoker_information_parser import SmokerInfoParser
from app.dto.pipeline.Smoker import Smoker


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

    def get_smoking_pattern_decision(self, text: str) -> Smoker:
        text = text.replace("(", " ")
        text = text.replace(")", " ")
        text = text.replace("/", " ")
        line = self.smoker_parser.get_parsed_info(text=text)
        print(line)
        if line != None:
            doc = self.nlp_algo(line.lower().strip())
            smoker = Smoker.DONT_KNOW
            for word in doc.ents:
                if str(word) in self.bag_of_words:
                    smoker = Smoker.NOT_SMOKER if word._.negex is True else Smoker.SMOKER
                    break
            return smoker
        return Smoker.DONT_KNOW
