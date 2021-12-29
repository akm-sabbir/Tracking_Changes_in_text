from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult


class icd10_meta_info(BasePipelineComponentResult):

    def __init__(self, hcc_map = '', score=0.0, entity_score=0.0, length=0, remove=False):
        self.hcc_map: str = hcc_map
        self.score: float = score
        self.entity_score: float = entity_score
        self.length: int = length
        self.remove: bool = remove