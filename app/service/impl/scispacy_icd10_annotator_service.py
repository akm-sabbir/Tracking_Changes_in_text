from typing import List

import spacy

from negspacy.termsets import termset

from app.dto.core.negation_patterns import NegationPatterns
from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.service.icd10_annotator_service import ICD10AnnotatorService
from app.service.impl.cui_to_icd10_service_impl import CUItoICD10ServiceImpl
from app.util.config_manager import ConfigManager
from app.util.dependency_injector import DependencyInjector
from scispacy.linking import EntityLinker  # do not remove
from app.util.negation_sentence_segmentation import set_custom_boundaries  # do not remove


class ScispacyICD10AnnotatorService(ICD10AnnotatorService):
    def __init__(self):
        self.__model_name = ConfigManager.get_specific_config("scispacy_umls_model_name", "umls_model_name")
        self.__umls_linker_name = ConfigManager.get_specific_config("scispacy_umls_linker_name", "umls_linker_name")

        self.nlp = spacy.load(self.__model_name)

        self.nlp.add_pipe("scispacy_linker", config={"resolve_abbreviations": True,
                                                     "linker_name": self.__umls_linker_name})

        # For negation
        self.nlp.add_pipe('set_custom_boundaries', first=True)

        self.__clinical_termset = termset("en_clinical")
        self.__clinical_termset.add_patterns({
            "preceding_negations": NegationPatterns.PRECEDING_NEGATIONS.value,
            "following_negations": NegationPatterns.FOLLOWING_NEGATIONS.value,
        })
        self.nlp.add_pipe("negex", config={"neg_termset": self.__clinical_termset.get_patterns()})

        self.icd10_mapper_service: CUItoICD10ServiceImpl = DependencyInjector.get_instance(CUItoICD10ServiceImpl)

    def get_icd_10_codes(self, text: str) -> List[ICD10AnnotationResult]:
        doc = self.nlp(text)
        entities = doc.ents

        return self._map_to_annotation_result_dto(entities)

    def _map_cui_to_icd10_code(self, umls_ents: list) -> List[ICD10Annotation]:
        return [ICD10Annotation(code=icd10,
                                description=self.icd10_mapper_service.get_umls_data_from_cui(cui_id).concept,
                                score=cui_score)
                for cui_id, cui_score in umls_ents if (icd10 := self.icd10_mapper_service.get_icd10_from_cui(cui_id))]

    def _map_to_annotation_result_dto(self, entities: tuple) -> List[ICD10AnnotationResult]:
        return [ICD10AnnotationResult(medical_condition=entity.text,
                                      begin_offset=entity.start_char, end_offset=entity.end_char,
                                      is_negated=entity._.negex,
                                      suggested_codes=self._map_cui_to_icd10_code(entity._.kb_ents))
                for entity in entities if entity._.kb_ents]
