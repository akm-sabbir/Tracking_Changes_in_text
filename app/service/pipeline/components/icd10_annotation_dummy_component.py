from typing import List

from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent


class ICD10AnnotationDummyComponent(BasePipelineComponent):
    DEPENDS_ON: List = []

    def run(self, annotation_results: dict) -> List[ICD10AnnotationResult]:
        icd10_annotation_1 = ICD10Annotation(code="A15.0", description="Tuberculosis of lung", score=0.7)
        icd10_annotation_2 = ICD10Annotation(code="A15.9", description="Respiratory tuberculosis unspecified",
                                             score=0.54)
        icd10_annotation_result_1 = ICD10AnnotationResult(medical_condition="Tuberculosis", begin_offset=12,
                                                          end_offset=24, is_negated=False,
                                                          suggested_codes=[icd10_annotation_1, icd10_annotation_2])

        icd10_annotation_3 = ICD10Annotation(code="J12.0", description="Adenoviral pneumonia", score=0.89)
        icd10_annotation_4 = ICD10Annotation(code="J12.89", description="Other viral pneumonia",
                                             score=0.45)

        icd10_annotation_result_2 = ICD10AnnotationResult(medical_condition="pneumonia", begin_offset=45, end_offset=54,
                                                          is_negated=True,
                                                          suggested_codes=[icd10_annotation_3, icd10_annotation_4])

        return [icd10_annotation_result_1, icd10_annotation_result_2]
