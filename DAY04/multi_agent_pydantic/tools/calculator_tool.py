## ==================================================================
##                 구조적 Tool 생성
## 목적: Input Schema와 Tool 함수 연결한 구조적 Tool 생성 및 등록
## ==================================================================

## ---------------------------------------
## 모듈 로딩
## ---------------------------------------
from __future__ import annotations
from langchain_core.tools import StructuredTool
from schemas.calc_schema import CalculatorInput


## ---------------------------------------
## Tool 함수
## ---------------------------------------
def _calculate(expression: str) -> str:
    """간단 계산기. 데모용이라 eval을 사용합니다(실서비스에서는 파서 권장)."""
    try:
        allowed = set("0123456789+-*/(). %")
        if any(ch not in allowed for ch in expression):
            return "Error: 허용되지 않은 문자가 포함되었습니다."
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Error: {e}"

## ---------------------------------------
## 구조적 Tool 생성 
## ---------------------------------------
calculator_tool = StructuredTool.from_function(
    name="calculator",
    description="수학 수식을 계산할 때 사용합니다. 입력은 expression 하나입니다.",
    args_schema=CalculatorInput,
    func=_calculate,
)
