from typing import List

from munch import munchify

from app.dto.core.icd10_pipeline_params import ICD10PipelineParams
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.dto.response.icd10_annotation_response import ICD10AnnotationResponse
from app.service.icd10_pipeline_service import ICD10PipelineService
from app.service.impl.dynamo_db_service import DynamoDbService
from app.service.pipeline.components.acm_icd10_annotation_component import ACMICD10AnnotationComponent
from app.service.pipeline.components.icd10_annotation_filter_component import ICD10AnnotationAlgoComponent
from app.service.pipeline.components.icd10_to_hcc_annotation import ICD10ToHccAnnotationComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent
from app.service.pipeline.pipeline_manager import PipelineManager
from app.util.config_manager import ConfigManager


class ICD10PipelineServiceImpl(ICD10PipelineService):
    def __init__(self):
        self.__pipeline_components = [NotePreprocessingComponent(), ACMICD10AnnotationComponent(),
                                      ICD10ToHccAnnotationComponent(), ICD10AnnotationAlgoComponent()]
        self.__pipeline_manager = PipelineManager(self.__pipeline_components)
        self.__db_service = DynamoDbService(ConfigManager.get_specific_config("aws", "annotation_table_name"))

    def run_icd10_pipeline(self, params: ICD10PipelineParams) -> ICD10AnnotationResponse:
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
        pipeline_result = self.__pipeline_manager.run_pipeline(id=params.note_id, text=params.text,
                                                               acm_cached_result=acm_cached_result,
                                                               dx_threshold=params.dx_threshold,
                                                               icd10_threshold=params.icd10_threshold,
                                                               parent_threshold=params.parent_threshold
                                                               )
        icd10_annotations: List[ICD10AnnotationResult] = pipeline_result[ICD10AnnotationAlgoComponent]
        return ICD10AnnotationResponse(
            id=params.note_id,
            icd10_annotations=icd10_annotations
        )
