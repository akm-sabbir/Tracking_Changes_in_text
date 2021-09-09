from abc import abstractmethod, ABC

from app.dto.response.icd10_annotation_response import ICD10AnnotationResponse


class ICD10AnnotatorService(ABC):
    @abstractmethod
    def annotate_icd_10(self, text: str) -> ICD10AnnotationResponse:
        raise NotImplementedError()
