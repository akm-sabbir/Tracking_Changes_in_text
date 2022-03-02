from typing import List

import spacy
from app.service.icd10_annotator_service import ICD10AnnotatorService


class ScispacyICD10AnnotatorService(ICD10AnnotatorService):
    def __init__(self, model_name: str, linker_name: str):
        self.nlp = spacy.load(model_name)

        self.nlp.add_pipe("scispacy_linker", config={"resolve_abbreviations": True, "linker_name": linker_name})

    def get_icd_10_codes(self, text: str) -> List:
        doc = self.nlp(text)

        entities = doc.ents

        return []