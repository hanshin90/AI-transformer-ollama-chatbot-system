# ==================================================================
# Tool 생성 - 다중 입력 Tool (검색 Tool)
#
# Agent가 top_k를 필요할 때만 선택적으로 사용
# 기본값은 자동 적용
# ==================================================================
# ==================================================================
# 모듈 로딩
# ==================================================================
from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool

# 1) 입력 스키마 정의
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

class WebSearchInput(BaseModel):
    query: str = Field(
        description="검색할 키워드"
    )
    top_k: int = Field(
        default=5,
        description="반환할 검색 결과 수 (기본값: 5)"
    )

def _web_search(query: str, top_k: int = 5) -> str:
    return f"[검색 결과] '{query}'에 대한 상위 {top_k}개 요약"

web_search = StructuredTool.from_function(
    func=_web_search,
    name="web_search",
    description="외부 정보나 일반적인 웹 검색이 필요할 때 사용",
    args_schema=WebSearchInput
)