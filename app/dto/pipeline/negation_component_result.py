from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult
from app.dto.core.service.Tokens import TokenInfo
from typing import List


class NegationResult(BasePipelineComponentResult):
    def __init__(self, token_info_with_span: List[TokenInfo]):
        self.tokens_with_span: str = token_info_with_span
