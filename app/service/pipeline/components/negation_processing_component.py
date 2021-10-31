
from collections import defaultdict
from typing import List

from app.dto.core.pipeline.acm_icd10_response import ACMICD10Result
from app.dto.core.pipeline.paragraph import Paragraph
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.dto.request.hcc_request_dto import HCCRequestDto
from app.dto.response.hcc_response_dto import HCCResponseDto
from app.service.hcc_service import HCCService
from app.service.pipeline.components.acm_icd10_annotation_component import ACMICD10AnnotationComponent
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent


class NegationHandlingComponent(BasePipelineComponent):

    DEPENDS_ON = [NotePreprocessingComponent]

    def run(self, annotation_results: dict) -> List[Paragraph]:
        if annotation_results['acm_cached_result'] is not None:
            return []
        paragraphs: List[Paragraph]= annotation_results[NotePreprocessingComponent]
        return paragraphs