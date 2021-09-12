from app.dto.base_dto import BaseDto


class ICD10Annotation(BaseDto):
    code: str
    description: str
    score: float
