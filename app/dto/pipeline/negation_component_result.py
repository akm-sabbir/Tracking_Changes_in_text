from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult
from app.dto.core.service.Tokens import TokenInfo
from typing import List


class NegationResult(BasePipelineComponentResult):
    tokens_with_span: List[TokenInfo]

    def __init__(self, token_info_with_span: List[TokenInfo]):
        self.tokens_with_span = token_info_with_span
