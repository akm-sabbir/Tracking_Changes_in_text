class ICD10PipelineParams:
    def __init__(self, note_id: str, text: str, dx_threshold: float, icd10_threshold: float,
                 parent_threshold: float, use_cache: bool):
        self.note_id = note_id
        self.text = text
        self.dx_threshold = dx_threshold
        self.icd10_threshold = icd10_threshold
        self.parent_threshold = parent_threshold
        self.use_cache = use_cache
