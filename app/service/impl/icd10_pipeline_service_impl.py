import asyncio
from functools import partial
from typing import List

from munch import munchify

from app.dto.core.icd10_pipeline_params import ICD10PipelineParams
from app.dto.core.pipeline.icd10_result import ICD10Result
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.dto.pipeline.smoker_condition import PatientSmokingCondition
from app.dto.response.hcc_response_dto import HCCResponseDto
from app.dto.response.icd10_annotation_response import ICD10AnnotationResponse
from app.service.icd10_pipeline_service import ICD10PipelineService
from app.service.impl.dynamo_db_service import DynamoDbService
from app.service.pipeline.components.acm_rxnorm_annotation_component import ACMRxNormAnnotationComponent
from app.service.pipeline.components.acmscimetamap_icd10_annotation_component import \
    ACMSciMetamapICD10AnnotationComponent
from app.service.pipeline.components.filtericd10_to_hcc_annotation import FilteredICD10ToHccAnnotationComponent
from app.service.pipeline.components.icd10_smoking_pattern_detection import PatientSmokingConditionDetectionComponent
from app.service.pipeline.components.icd10_token_to_graph_generation_component import TextToGraphGenerationComponent
from app.service.pipeline.components.medication_section_extractor_component import MedicationSectionExtractorComponent
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent
from app.service.pipeline.components.section_exclusion_service_component import SectionExclusionServiceComponent
from app.service.pipeline.components.subjective_section_extractor_component import SubjectiveSectionExtractorComponent
from app.service.pipeline.components.icd10_smoking_pattern_detection import PatientSmokingConditionDetectionComponent
from app.service.pipeline.components.icd10_tokenizing_text_component import TextTokenizationComponent
from app.service.pipeline.components.icd10_text_reconstruction_component import TextReconstructionComponent
from app.service.pipeline.pipeline_manager import PipelineManager
from app.settings import Settings
from app.util.config_manager import ConfigManager


class ICD10PipelineServiceImpl(ICD10PipelineService):

    def __init__(self):
        self.__pipeline_components = [PatientSmokingConditionDetectionComponent(Settings.get_nlp_smoker_detector()),
                                      SectionExclusionServiceComponent(),
                                      SubjectiveSectionExtractorComponent(), MedicationSectionExtractorComponent(),
                                      TextTokenizationComponent(),
                                      TextToGraphGenerationComponent(),
                                      NegationHandlingComponent(), TextReconstructionComponent(),NotePreprocessingComponent(),
                                      ACMSciMetamapICD10AnnotationComponent(),
                                      FilteredICD10ToHccAnnotationComponent()]

        self.__pipeline_manager = PipelineManager(self.__pipeline_components)
        self.__db_service = DynamoDbService(ConfigManager.get_specific_config("aws", "annotation_table_name"))

    async def run_icd10_pipeline(self, params: ICD10PipelineParams) -> ICD10AnnotationResponse:
        if params.use_cache:
            acm_cached_response = self.__db_service.get_item(params.note_id)
        else:
            acm_cached_response = []
        if len(acm_cached_response) == 1:
            acm_response: dict = acm_cached_response[0]
            acm_cached_result = [
                munchify(acm_response)
            ]
        else:
            acm_cached_result = None

        run_pipeline_func = partial(self.__pipeline_manager.run_pipeline, id=params.note_id, text=params.text,
                                    acm_cached_result=acm_cached_result,
                                    dx_threshold=params.dx_threshold,
                                    icd10_threshold=params.icd10_threshold,
                                    parent_threshold=params.parent_threshold,
                                    patient_info=params.patient_info,
                                    changed_words={})

        pipeline_result = await asyncio.get_running_loop().run_in_executor(None, run_pipeline_func)

        icd10_annotations: List[ICD10AnnotationResult] = pipeline_result[ACMSciMetamapICD10AnnotationComponent][0].icd10_annotations
        hcc_maps: HCCResponseDto = pipeline_result[FilteredICD10ToHccAnnotationComponent][0]
        acm_annotation_result: ICD10Result = pipeline_result[ACMSciMetamapICD10AnnotationComponent][0]
        smoking_condition: PatientSmokingCondition = pipeline_result[PatientSmokingConditionDetectionComponent][0]

        return ICD10AnnotationResponse(
            id=params.note_id,
            icd10_annotations=icd10_annotations,
            raw_acm_data=acm_annotation_result.raw_acm_data,
            hcc_maps=hcc_maps,
            is_smoker=smoking_condition.isSmoker
        )
