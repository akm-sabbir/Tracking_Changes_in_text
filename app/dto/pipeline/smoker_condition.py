from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult


class PatientSmokingCondition(BasePipelineComponentResult):
    notSmoker: bool

    def __init__(self, smoker=False):
        self.notSmoker = smoker
