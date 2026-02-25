# ==================================================================
# Tool 실패(Error)도 JSON으로 “표준화"
# ==================================================================
# -> Tool 실패가 Agent 전체를 죽이지 않도록 설계
# -> “관찰 가능한 실패”를 만드는 실무 습관
# ==================================================================
# ==================================================================
# 모듈 로딩
# ==================================================================
from langchain_core.tools import tool

# ==================================================================
# Tool 생성
# -> 예외가 그대로 터질 수 있음
# ==================================================================
from langchain_core.tools import tool

@tool
def divide(a: float, b: float) -> str:
    """나눗셈을 수행한다."""
    return str(a / b)



# ==================================================================
# Tool 개선
# -> 모든 Tool은 성공/실패 모두 JSON 문자열로 반환
# -> 실패 시에도 프로그램이 죽지 않고, 다음 단계가 가능
# -> 표준 에러 포맷 통일
# ==================================================================
import json
from langchain_core.tools import tool

@tool
def divide(a: float, b: float) -> str:
    """
    [언제 사용?] 두 수의 나눗셈이 필요할 때 사용한다.
    [출력] 성공/실패 모두 JSON 문자열로 반환한다.
    """
    try:
        result = a / b
        return json.dumps({
            "tool": "divide",
            "ok": True,
            "data": {"a": a, "b": b, "result": result}
        }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({
            "tool": "divide",
            "ok": False,
            "error": {"type": type(e).__name__, "message": str(e)}
        }, ensure_ascii=False)