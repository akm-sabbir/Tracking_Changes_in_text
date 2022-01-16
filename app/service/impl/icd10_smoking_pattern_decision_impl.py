import spacy

from app.service.icd10_smoking_pattern_service import ICD10SmokingPatternDetection
from app.util.smoker_information_parser import SmokerInfoParser
import os
import codecs


class ICD10SmokingPatternDecisionImpl(ICD10SmokingPatternDetection):
    smoker_parser: SmokerInfoParser = SmokerInfoParser()
    path_name = "/home/akm.sabbir/ML_Projects/mongodb_data/Medant-Gold-Dataset/notes"
    bag_of_words = set(["smokers", "smoker", "smoke", "smoking", "smoked", "tobacco", "tobaco"])
    nlp_algo: spacy.Language

    def __init__(self, nlp=None):
        self.nlp_algo = nlp

    def get_smoking_pattern_decision(self, text: str) -> bool:
        line = self.smoker_parser.get_parsed_info(text=text)
        if line != None:
            doc = self.nlp_algo(line.lower())
            smoker = False
            for word in doc.ents:
                if str(word) in self.bag_of_words:

                    smoker = True if word._.negex is True else False
                    break
            return smoker
        return False

    def get_data_from_file(self):
        file_names = os.listdir(self.path_name)
        for each_name in file_names:
            with codecs.open(os.path.join(self.path_name, each_name)) as data_reader:
                text = data_reader.read()
                line = self.smoker_parser.get_parsed_info(text=text)
                if line is not None:
                    print(self.get_smoking_pattern_decision(line))
