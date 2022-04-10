from typing import List, Tuple, Dict

import boto3

from app.dto.pipeline.rxnorm_annotation import RxNormAnnotation
from app.dto.pipeline.rxnorm_annotation_result import RxNormAnnotationResult
from app.dto.pipeline.rxnorm_attribute_annotation import RxNormAttributeAnnotation
from app.exception.service_exception import ServiceException
from app.service.rxnorm_annotator_service import RxNormAnnotatorService


class AmazonRxNormAnnotatorServiceImpl(RxNormAnnotatorService):
    def __init__(self):
        self.__client = boto3.client(service_name='comprehendmedical')

    def get_rxnorm_codes(self, text: str) -> Tuple[List[Dict], List[RxNormAnnotationResult]]:
        try:
            result = self.__client.infer_rx_norm(Text=text)
        except Exception:
            raise ServiceException(message="Error getting RxNorm annotation from ACM")

        rxnorm_entities = result['Entities']

        return rxnorm_entities, [self.__map_to_rxnorm_dto(rxnorm_entity) for rxnorm_entity in rxnorm_entities]

    def __map_to_rxnorm_dto(self, rxnorm_entity: dict) -> RxNormAnnotationResult:
        text = rxnorm_entity['Text']
        rxnorm_type = rxnorm_entity['Type']
        score = rxnorm_entity['Score']
        begin_offset = rxnorm_entity['BeginOffset']
        end_offset = rxnorm_entity['EndOffset']
        is_negated = "NEGATION" in [trait["Name"] for trait in rxnorm_entity["Traits"]]
        attributes = [
            RxNormAttributeAnnotation(score=attribute['Score'], attribute_type=attribute['Type'],
                                      relationship_score=attribute['RelationshipScore'],
                                      id=attribute['Id'], begin_offset=attribute['BeginOffset'],
                                      end_offset=attribute['EndOffset'], text=attribute['Text']
                                      )
            for attribute in rxnorm_entity['Attributes']
        ]
        suggested_codes = [
            RxNormAnnotation(code=concept['Code'], description=concept['Description'], score=concept['Score'])
            for concept in rxnorm_entity['RxNormConcepts']
        ]
        return RxNormAnnotationResult(medication=text, rxnorm_type=rxnorm_type, attributes=attributes, score=score,
                                      begin_offset=begin_offset, end_offset=end_offset,
                                      is_negated=is_negated, suggested_codes=suggested_codes)
