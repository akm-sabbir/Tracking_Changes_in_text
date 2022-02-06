from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult


class PatientSmokingCondition(BasePipelineComponentResult):
    isSmoker: int

    def __init__(self, smoker=-1):
        self.isSmoker = smoker
