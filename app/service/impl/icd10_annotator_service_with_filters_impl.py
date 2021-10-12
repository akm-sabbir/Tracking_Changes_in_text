from abc import abstractmethod, ABC
from typing import List

from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.exception.service_exception import ServiceException
from app.service.icd10_annotator_service_with_filters import ICD10AnnotatorServiceWithFilter
import operator


class ICD10AnnotatorServiceWithFilterImpl(ICD10AnnotatorServiceWithFilter):

    def get_icd_10_filtered_codes(self, text: str, dx_threshold: float, icd10_threshod: float,
                                  parent_threshold: float) -> List:
        try:
            result = self.__client.infer_icd10_cm(Text=text)
        except Exception:
            raise ServiceException(message="Error getting ICD10 annotation from ACM")
        icd_10_entities = result['Entities']
        icd_10_entities = self.apply_dx_threshold(icd_10_entities=icd_10_entities, dx_thresh=dx_threshold,
                                                  operate=operator.gt)
        return [self.__map_to_icd_dto(icd_10_entity) for icd_10_entity in icd_10_entities]

    def apply_dx_threshold(self,icd_10_entities: list[dict], dx_thresh: float, operate) -> list:
        return [icd_10_entity for icd_10_entity in icd_10_entities if operate(icd_10_entity['Score'], dx_thresh)]

    def __map_to_icd_dto(self, icd_10_entity: dict) -> ICD10AnnotationResult:
        text = icd_10_entity['Text']
        begin_offset = icd_10_entity['BeginOffset']
        end_offset = icd_10_entity['EndOffset']
        is_negated = "NEGATION" in [trait["Name"] for trait in icd_10_entity["Traits"]]
        suggested_codes = [
            ICD10Annotation(code=concept['Code'], description=concept['Description'], score=concept['Score'])
            for concept in icd_10_entity['ICD10CMConcepts']
        ]
        return ICD10AnnotationResult(medical_condition=text, begin_offset=begin_offset, end_offset=end_offset,
                                     is_negated=is_negated, suggested_codes=suggested_codes)