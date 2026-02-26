from pydantic import BaseModel, Field

class CalcInput(BaseModel):
    expression: str = Field(..., description="계산할 수식")
