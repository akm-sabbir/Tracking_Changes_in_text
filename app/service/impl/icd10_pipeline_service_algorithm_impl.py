from app.dto.response.icd10_annotation_response import ICD10AnnotationResponse
from app.service.icd10_pipeline_service_with_filters import  ICD10PipelineServiceWithFilter
from app.service.pipeline.components.icd10_annotation_component import ICD10AnnotationComponent
from app.service.pipeline.components.icd10_to_hcc_annotation import ICD10ToHccAnnotationComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent
from app.service.pipeline.components.icd10_annotation_filter_component import ICD10AnnotationAlgoComponent
from app.service.pipeline.pipeline_manager import PipelineManager
from collections import namedtuple
from collections import defaultdict


class ICD10PipelineServiceAlgoImpl(ICD10PipelineServiceWithFilter):
    def __init__(self):
        self.__pipeline_components = [NotePreprocessingComponent(), ICD10AnnotationComponent(),
                                      ICD10ToHccAnnotationComponent(), ICD10AnnotationAlgoComponent()]
        self.__pipeline_manager = PipelineManager(self.__pipeline_components)

    def run_icd10_pipeline(self, text: str, dx_threshold: float = 0.5,
                           icd10_threshold: float = 0.5,
                           parent_threshold: float = 0.5) -> ICD10AnnotationResponse:
        pipeline_result = self.__pipeline_manager.run_pipeline(text=text,
                                                               dx_threshold=dx_threshold,
                                                               icd10_threshold=icd10_threshold,
                                                               parent_threshold=parent_threshold)
        print(pipeline_result[ICD10AnnotationAlgoComponent])
        return ICD10AnnotationResponse(
            icd10_annotations=pipeline_result[ICD10AnnotationAlgoComponent]
        )
