from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult


class GraphTokenResult(BasePipelineComponentResult):
    def __init__(self, graph_container: dict):
        self.graph_token_container: dict = graph_container
