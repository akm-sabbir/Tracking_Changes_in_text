import re
from typing import List, Dict

from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.service.icd10_annotator_service import ICD10AnnotatorService
from app.service.impl.cui_to_icd10_service_impl import CUItoICD10ServiceImpl
from app.util.config_manager import ConfigManager
from app.util.dependency_injector import DependencyInjector
from app.util.rest_client_util import RestClientUtil


class PymetamapICD10AnnotatorService(ICD10AnnotatorService):

    def __init__(self):
        self.icd10_mapper_service: CUItoICD10ServiceImpl = DependencyInjector.get_instance(CUItoICD10ServiceImpl)

    def get_icd_10_codes(self, text: str) -> List:
        metamap_service_url = ConfigManager.get_specific_config("metamap", "service_url")
        request_data = {'text': text}
        metamap_response = RestClientUtil.post_sync(url=metamap_service_url, req_dto=request_data)
        return self._map_to_annotation_result_dto(text, metamap_response.json())

    def _map_to_annotation_result_dto(self, text: str, concepts) -> List[ICD10AnnotationResult]:
        unique_concepts: Dict[str, ICD10AnnotationResult] = {}
        for concept in concepts:
            if "mm" not in concept:
                continue
            icd10_data = self.icd10_mapper_service.get_umls_data_from_cui(concept["cui"])
            if icd10_data.icd10 == "":
                continue
            icd10_annotations = [ICD10Annotation(code=icd10_data.icd10,
                                                 description=icd10_data.concept,
                                                 score=concept["score"])]

            # position info is separated by ; . We take the first position info only
            position_string = concept["posInfo"].split(";")[0]
            if position_string in unique_concepts:
                unique_concepts[position_string].suggested_codes.extend(icd10_annotations)
                continue

            # position info can be 12/3 or 12/5,11/7 or [12/3],# [12/5,11/7]. Here, for 12/3 , 12 - index, 3 - length
            position_info_pattern = r"\[?(([0-9]+/[0-9]+),?)+]?"
            pos_info = re.search(position_info_pattern, position_string).group()

            # remove brackets
            pos_info = pos_info.replace("[", "")
            pos_info = pos_info.replace("]", "")

            # find only positional info (12/3, 11/5)
            position_pattern = r"[0-9]+/[0-9]+"
            positions = list(re.finditer(position_pattern, pos_info))

            # first positional info is the start index
            start_position_info = positions[0].group()
            start_position = int(start_position_info.split("/")[0]) - 1

            # the last info is the end index
            end_position_info = positions[-1].group()
            end_position = int(end_position_info.split("/")[0]) + int(end_position_info.split("/")[1]) - 1

            medical_condition = text[start_position:end_position]

            icd10_annotation_result = ICD10AnnotationResult(medical_condition=medical_condition,
                                                            begin_offset=start_position, end_offset=end_position,
                                                            is_negated=False, suggested_codes=icd10_annotations)

            unique_concepts[position_string] = icd10_annotation_result
        return list(unique_concepts.values())
