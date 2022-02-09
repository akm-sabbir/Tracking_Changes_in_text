from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult
from app.dto.pipeline.Smoker import Smoker


class PatientSmokingCondition(BasePipelineComponentResult):
    isSmoker: Smoker

    def __init__(self, smoker=Smoker.DONT_KNOW):
        self.isSmoker = smoker
