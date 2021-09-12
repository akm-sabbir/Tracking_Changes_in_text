from fastapi import APIRouter

from app.dto.request.icd10_annotation_request import ICD10AnnotationRequest
from app.dto.response.icd10_annotation_response import ICD10AnnotationResponse
from app.service.icd10_annotator_service import ICD10AnnotatorService
from app.service.impl.icd10_annotator_service_impl import ICD10AnnotatorServiceImpl
from app.util.dependency_injector import DependencyInjector

router = APIRouter()
prefix = "/annotation"

__icd10_service: ICD10AnnotatorService = DependencyInjector.get_instance(ICD10AnnotatorServiceImpl)


@router.post(path="/icd10", response_model=ICD10AnnotationResponse)
async def annotate_icd_10(icd10_annotation_request: ICD10AnnotationRequest) -> ICD10AnnotationResponse:
    return __icd10_service.annotate_icd_10(icd10_annotation_request.text)
