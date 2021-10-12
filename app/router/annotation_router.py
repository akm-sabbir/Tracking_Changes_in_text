from fastapi import APIRouter

from app.dto.request.icd10_annotation_request import ICD10AnnotationRequest
from app.dto.response.icd10_annotation_response import ICD10AnnotationResponse
from app.service.impl.icd10_pipeline_service_impl import ICD10PipelineServiceImpl
from app.util.dependency_injector import DependencyInjector

router = APIRouter()
prefix = "/annotation"

__icd10_service: ICD10PipelineServiceImpl = DependencyInjector.get_instance(ICD10PipelineServiceImpl)


@router.post(path="/icd10", response_model=ICD10AnnotationResponse)
async def annotate_icd_10(icd10_annotation_request: ICD10AnnotationRequest) -> ICD10AnnotationResponse:
    return __icd10_service.run_icd10_pipeline(icd10_annotation_request.text)


@router.post(path="/icd10/dx_icd_filter", response_model=ICD10AnnotationResponse)
async def annotate_icd_10_by_filter(icd10_annotation_request: ICD10AnnotationRequest) -> ICD10AnnotationResponse:
    return __icd10_service.run_icd10_pipeline(icd10_annotation_request.text)
