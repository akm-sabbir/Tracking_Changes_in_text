from typing import List, Optional

from pydantic import Field

from app.dto.base_dto import BaseDto


class HCCRequestDto(BaseDto):
    icd_codes_list: List
    age: Optional[float] = 70
    eligibility: Optional[str] = Field("CNA", regex="^(CPA|CPD|CNA|CND|INS|CFA|CFD|NE|SNPNE)$")
    medicaid: Optional[bool] = True
    original_reason_for_entitlement: Optional[str] = Field("0", regex="^(0|1|2|3)$")
    sex: Optional[str] = Field("M", regex="^(M|F)$")
