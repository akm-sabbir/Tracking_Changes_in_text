from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult


class PatientSmokingCondition(BasePipelineComponentResult):
    isSmoker: bool

    def __init__(self, smoker=False):
        self.isSmoker = smoker
