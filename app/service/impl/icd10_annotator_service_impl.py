from app.dto.response.icd10_annotation_response import ICD10AnnotationResponse
from app.service.icd10_annotator_service import ICD10AnnotatorService
from app.service.pipeline.components.dummy_component_one import DummyComponentOne
from app.service.pipeline.components.dummy_component_three import DummyComponentThree
from app.service.pipeline.components.dummy_component_two import DummyComponentTwo
from app.service.pipeline.pipeline_manager import PipelineManager


class ICD10AnnotatorServiceImpl(ICD10AnnotatorService):
    def __init__(self):
        self.__pipeline_components = [DummyComponentOne(), DummyComponentTwo(), DummyComponentThree()]
        self.__pipeline_manager = PipelineManager(self.__pipeline_components)

    def annotate_icd_10(self, text: str) -> ICD10AnnotationResponse:
        pipeline_result = self.__pipeline_manager.run_pipeline(text=text)
        return ICD10AnnotationResponse(
            icd10_annotations=[pipeline_result[DummyComponentOne], pipeline_result[DummyComponentTwo],
                               pipeline_result[DummyComponentThree]]
        )
