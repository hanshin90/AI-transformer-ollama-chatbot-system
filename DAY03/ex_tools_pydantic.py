# ==================================================================
# Tool 생성
# -> pip install -U email-validator
# ==================================================================
# ==================================================================
# 모듈 로딩
# ==================================================================
from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool

# 1) 입력 스키마 정의 : 유효성 검사(정해진 규칙에 맞는 데이터 여부 체크용)
class CalculatorInput(BaseModel):
    expression: str = Field(
        description="계산할 수식 문자열. 예: '12*(3+4)'"
    )

# 2) 실제 실행 함수
def _calculator(expression: str) -> str:
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

# 3) Tool 생성
calculator = StructuredTool.from_function(
    func=_calculator,
    name="calculator",
    description="수학 계산이 필요할 때 사용하는 계산기",
    args_schema=CalculatorInput
)

