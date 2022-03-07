from typing import List

import spacy

from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.service.icd10_annotator_service import ICD10AnnotatorService
from app.service.impl.cui_to_icd10_service_impl import CUItoICD10ServiceImpl
from app.util.dependency_injector import DependencyInjector
from scispacy.linking import *


class ScispacyICD10AnnotatorService(ICD10AnnotatorService):
    def __init__(self, model_name: str, linker_name: str):
        self.nlp = spacy.load(model_name)

        self.nlp.add_pipe("scispacy_linker", config={"resolve_abbreviations": True, "linker_name": linker_name})
        self.icd10_mapper_service: CUItoICD10ServiceImpl = DependencyInjector.get_instance(CUItoICD10ServiceImpl)

    def get_icd_10_codes(self, text: str) -> List[ICD10AnnotationResult]:
        doc = self.nlp(text)
        entities = doc.ents

        return self._map_to_annotation_result_dto(entities)

    def _map_cui_to_icd10_code(self, umls_ents: list) -> List[ICD10Annotation]:
        return [ICD10Annotation(code=self.icd10_mapper_service.get_icd10_from_cui(cui_id),
                                description=self.icd10_mapper_service.get_umls_data_from_cui(cui_id).concept,
                                score=cui_score)
                for cui_id, cui_score in umls_ents]

    def _map_to_annotation_result_dto(self, entities: tuple) -> List[ICD10AnnotationResult]:
        return [ICD10AnnotationResult(medical_condition=entity.text,
                                      begin_offset=entity.start_char, end_offset=entity.end_char,
                                      is_negated=False, suggested_codes=self._map_cui_to_icd10_code(entity._.kb_ents))
                for entity in entities if entity._.kb_ents]
