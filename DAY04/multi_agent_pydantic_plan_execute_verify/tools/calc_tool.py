from langchain_core.tools import StructuredTool
from schemas.calc_schema import CalcInput

def _calc(expression: str) -> str:
    return str(eval(expression, {"__builtins__": {}}, {}))

calc_tool = StructuredTool.from_function(
    name="calculator",
    description="수식 계산 도구",
    args_schema=CalcInput,
    func=_calc,
)
