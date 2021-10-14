from collections import namedtuple

from app.dto.core.pipeline.acm_icd10_response import ACMICD10Result
from app.dto.response.icd10_annotation_response import ICD10AnnotationResponse
from app.service.icd10_pipeline_service import ICD10PipelineService
from app.service.impl.dynamo_db_service import DynamoDbService
from app.service.pipeline.components.acm_icd10_annotation_component import ACMICD10AnnotationComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent
from app.service.pipeline.pipeline_manager import PipelineManager
from app.util.config_manager import ConfigManager


class ICD10PipelineServiceImpl(ICD10PipelineService):
    def __init__(self):
        self.__pipeline_components = [NotePreprocessingComponent(), ACMICD10AnnotationComponent()]
        self.__pipeline_manager = PipelineManager(self.__pipeline_components)
        self.__db_service = DynamoDbService(ConfigManager.get_specific_config("aws", "annotation_table_name"))

    def run_icd10_pipeline(self, note_id: str, text: str) -> ICD10AnnotationResponse:
        acm_cached_response = self.__db_service.get_item(note_id)
        if len(acm_cached_response) == 1:
            acm_response: dict = acm_cached_response[0]
            acm_cached_result = [
                namedtuple('ACMICD10Result', acm_response.keys())(*acm_response.values())]
        else:
            acm_cached_result = None
        pipeline_result = self.__pipeline_manager.run_pipeline(id=note_id, text=text,
                                                               acm_cached_result=acm_cached_result)
        acm_response: ACMICD10Result = pipeline_result[ACMICD10AnnotationComponent][0]
        return ICD10AnnotationResponse(
            id=note_id,
            icd10_annotations=acm_response.icd10_annotations
        )
