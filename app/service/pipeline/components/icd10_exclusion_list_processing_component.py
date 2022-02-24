from collections import defaultdict
from typing import List

from app.dto.core.pipeline.acm_icd10_response import ACMICD10Result
from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.dto.response.hcc_response_dto import HCCResponseDto
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.impl.icd10_exclusion_list_processing_service_impl import Icd10CodeExclusionServiceImpl
from app.settings import Settings
from app.util.dependency_injector import DependencyInjector
from app.service.icd10_negation_service import ICD10NegationService
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent
from app.service.pipeline.components.acm_icd10_annotation_component import ACMICD10AnnotationComponent
from app.service.pipeline.components.icd10_to_hcc_annotation import ICD10ToHccAnnotationComponent
from app.util.icd_exclusions import ICDExclusions


class CodeExclusionHandlingComponent(BasePipelineComponent):
    DEPENDS_ON = [NegationHandlingComponent, NotePreprocessingComponent,
                  ACMICD10AnnotationComponent, ICD10ToHccAnnotationComponent]
    __icd10_exclusion_handling_service: Icd10CodeExclusionServiceImpl = Icd10CodeExclusionServiceImpl(
<<<<<<< HEAD
        ICDExclusions(exclusions_json_dict=Settings.get_exclusion_dict()))
=======
        ICDExclusions(exclusions_json=Settings.get_exclusion_dict()))
>>>>>>> bugfix/PA-1007-missing-acm-annnotations-updating-exclusion-service-algorithm

    def __init__(self):
        super().__init__()

    def run(self, annotation_results: dict) -> List[ACMICD10Result]:
        acm_result: List[ACMICD10Result] = annotation_results[ACMICD10AnnotationComponent]
        annotated_list: List[ICD10AnnotationResult] = acm_result[0].icd10_annotations
        icd10_meta_info: dict = annotation_results[ICD10ToHccAnnotationComponent][0].hcc_meta_map_info
        icd10_meta_info = self.__icd10_exclusion_handling_service.get_icd_10_code_exclusion_decision(icd10_meta_info)
        for annotation_entity in annotated_list:
            annotation_entity.suggested_codes: List[ICD10Annotation] \
                = [icd10 for icd10 in annotation_entity.suggested_codes
                   if icd10_meta_info[icd10.code.replace(".", "")].remove is not True]
        acm_result[0].icd10_annotations = annotated_list
        return acm_result
