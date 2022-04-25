from collections import defaultdict
from typing import List

from app.dto.core.pipeline.icd10_result import ICD10Result
from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.dto.response.hcc_response_dto import HCCResponseDto
from app.service.pipeline.components.acm_rxnorm_annotation_component import ACMRxNormAnnotationComponent
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.impl.icd10_exclusion_list_processing_service_impl import Icd10CodeExclusionServiceImpl
from app.service.pipeline.components.icd10_smoking_pattern_detection import PatientSmokingConditionDetectionComponent
from app.service.pipeline.components.medication_section_extractor_component import MedicationSectionExtractorComponent
from app.service.pipeline.components.section_exclusion_service_component import SectionExclusionServiceComponent
from app.service.pipeline.components.subjective_section_extractor_component import SubjectiveSectionExtractorComponent
from app.settings import Settings
from app.util.dependency_injector import DependencyInjector
from app.service.icd10_negation_service import ICD10NegationService
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent
from app.service.pipeline.components.acmscimetamap_icd10_annotation_component import ACMSciMetamapICD10AnnotationComponent
from app.service.pipeline.components.icd10_tokenizing_text_component import TextTokenizationComponent
from app.service.pipeline.components.icd10_to_hcc_annotation import ICD10ToHccAnnotationComponent
from app.util.icd_exclusions import ICDExclusions


class CodeExclusionHandlingComponent(BasePipelineComponent):
    DEPENDS_ON = [PatientSmokingConditionDetectionComponent,
                                      SectionExclusionServiceComponent,
                                      SubjectiveSectionExtractorComponent, MedicationSectionExtractorComponent,
                                      TextTokenizationComponent,
                                      NegationHandlingComponent, NotePreprocessingComponent,
                                      ACMSciMetamapICD10AnnotationComponent,
                                       ICD10ToHccAnnotationComponent]
    __icd10_exclusion_handling_service: Icd10CodeExclusionServiceImpl = Icd10CodeExclusionServiceImpl(
        ICDExclusions(exclusions_json_dict=Settings.get_exclusion_dict()))

    def __init__(self):
        super().__init__()

    def run(self, annotation_results: dict) -> List[ICD10Result]:
        acm_result: List[ICD10Result] = annotation_results[ACMSciMetamapICD10AnnotationComponent]
        annotated_list: List[ICD10AnnotationResult] = acm_result[0].icd10_annotations
        icd10_meta_info: dict = annotation_results[ICD10ToHccAnnotationComponent][0].hcc_meta_map_info
        icd10_meta_info = self.__icd10_exclusion_handling_service.get_icd_10_code_exclusion_decision(icd10_meta_info)
        for annotation_entity in annotated_list:
            annotation_entity.suggested_codes: List[ICD10Annotation] \
                = [icd10 for icd10 in annotation_entity.suggested_codes
                   if icd10_meta_info[icd10.code.replace(".", "")].remove is not True]
        acm_result[0].icd10_annotations = annotated_list
        return acm_result
