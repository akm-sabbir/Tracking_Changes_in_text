import asyncio
from typing import List, Awaitable

from fastapi import APIRouter
from fastapi.params import Param

from app.settings import Settings
from app.dto.core.icd10_pipeline_params import ICD10PipelineParams
from app.dto.core.patient_info import PatientInfo
from app.dto.request.icd10_annotation_request import ICD10AnnotationRequest
from app.dto.response.icd10_annotation_response import ICD10AnnotationResponse
from app.service.impl.icd10_pipeline_service_impl import ICD10PipelineServiceImpl
from app.util.dependency_injector import DependencyInjector

router = APIRouter()
prefix = "/annotation"

__icd10_service: ICD10PipelineServiceImpl = DependencyInjector.get_instance(ICD10PipelineServiceImpl)


@router.post(path="/icd10", response_model=List[ICD10AnnotationResponse])
async def annotate_icd_10(icd10_annotation_requests: List[ICD10AnnotationRequest],
                          dx_threshold: float = Param(alias="dxThreshold", default=Settings.dx_threshold),
                          icd10_threshold: float = Param(alias="icd10Threshold", default=Settings.icd10_threshold),
                          parent_threshold: float = Param(alias="parentThreshold",
                                                          default=Settings.parent_threshold),
                          use_cache: bool = Param(alias="useCache",
                                                  default=Settings.use_cache)) -> List[ICD10AnnotationResponse]:
    tasks: List[Awaitable] = []
    for annotation_request in icd10_annotation_requests:
        patient_info = PatientInfo(annotation_request.age, annotation_request.sex)
        pipeline_params = ICD10PipelineParams(annotation_request.id, annotation_request.text, dx_threshold,
                                              icd10_threshold, parent_threshold, use_cache, patient_info)
        tasks.append(asyncio.create_task(__icd10_service.run_icd10_pipeline(pipeline_params)))

    response: List[ICD10AnnotationResponse] = [item for item in await asyncio.gather(*tasks)]

    return response
