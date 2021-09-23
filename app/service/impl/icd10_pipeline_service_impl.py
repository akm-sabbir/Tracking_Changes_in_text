from app.dto.response.icd10_annotation_response import ICD10AnnotationResponse
from app.service.icd10_pipeline_service import ICD10PipelineService
from app.service.pipeline.components.dummy_component_one import DummyComponentOne
from app.service.pipeline.components.dummy_component_two import DummyComponentTwo
from app.service.pipeline.components.icd10_annotation_dummy_component import ICD10AnnotationDummyComponent
from app.service.pipeline.pipeline_manager import PipelineManager


class ICD10PipelineServiceImpl(ICD10PipelineService):
    def __init__(self):
        self.__pipeline_components = [DummyComponentOne(), DummyComponentTwo(), ICD10AnnotationDummyComponent()]
        self.__pipeline_manager = PipelineManager(self.__pipeline_components)

    def run_icd10_pipeline(self, text: str) -> ICD10AnnotationResponse:
        pipeline_result = self.__pipeline_manager.run_pipeline(text=text)
        return ICD10AnnotationResponse(
            icd10_annotations=pipeline_result[ICD10AnnotationDummyComponent]
        )
