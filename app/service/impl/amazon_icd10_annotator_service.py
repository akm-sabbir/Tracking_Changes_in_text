from typing import List, Tuple, Dict

import boto3

from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.exception.service_exception import ServiceException
from app.service.icd10_annotator_service import ICD10AnnotatorService


class AmazonICD10AnnotatorServiceImpl(ICD10AnnotatorService):

    def __init__(self):
        KEY_='AKIASDZNPBJOOBDEH7HB'
        SECRET_KEY_='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'
        session = boto3.Session(
                                aws_access_key_id=KEY_,
                                aws_secret_access_key=SECRET_KEY_)
        self.__client = session.client(service_name='comprehendmedical', region_name='us-west-2')

    def get_icd_10_codes(self, text: str) -> Tuple[List[Dict], List[ICD10AnnotationResult]]:
        try:
            result = self.__client.infer_icd10_cm(Text=text.lower())
        except Exception:
            raise ServiceException(message="Error getting ICD10 annotation from ACM")
        icd_10_entities = result['Entities']
        return icd_10_entities, [self.__map_to_icd_dto(icd_10_entity, text) for icd_10_entity in icd_10_entities]

    def __map_to_icd_dto(self, icd_10_entity: dict, full_text: str) -> ICD10AnnotationResult:
        score = icd_10_entity['Score']
        begin_offset = icd_10_entity['BeginOffset']
        end_offset = icd_10_entity['EndOffset']
        text = full_text[begin_offset:end_offset]
        is_negated = "NEGATION" in [trait["Name"] for trait in icd_10_entity["Traits"]]
        suggested_codes = [
            ICD10Annotation(code=concept['Code'], description=concept['Description'], score=concept['Score'])
            for concept in icd_10_entity['ICD10CMConcepts']
        ]
        return ICD10AnnotationResult(medical_condition=text, score=score, begin_offset=begin_offset,
                                     end_offset=end_offset,
                                     is_negated=is_negated, suggested_codes=suggested_codes)
