# ==================================================================
# Tool 만들기
# ---------------------------------------------------------
# 요구사항:
#   - pip install -U langchain langchain-core langchain-community
#
# 실행:
#   python tools.py
# ==================================================================
# 모듈 로딩
# ==================================================================
from langchain_core.tools import tool


# ==================================================================
# 함수이름 : calculator
# 함수기능 : 수학 계산이 필요할 때 사용하는 계산기
#           입력 예: "3 * (4 + 5)"
# @tool   decorator → Schema 자동 생성
# @tool   docstring을 Tool의 설명서(description)로 사용
#         Agent는 이 설명서를 보고 언제 이 도구를 쓸지 결정
# ==================================================================
@tool("calculator")
def calculator(expression: str) -> str:
    """수학 수식을 계산. 예: '3*(4+5)' 또는 '12/4'"""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"



@tool
def TOOL_NAME(arg1: str, arg2: int = 5) -> str:
    """
    [언제 사용?] 어떤 상황에서 이 Tool을 반드시 사용해야 하는지 1~2문장
    [입력] arg1: 무엇 / 형식 / 예시, arg2: 의미 / 범위
    [출력] 무엇을 반환하는지
    [주의] 금지/제약/실패 조건 (짧게)
    """

@tool
def calculator(expression: str) -> str:
    """
    [언제 사용?] 수학 계산(사칙연산/괄호/비율)이 필요하면 사용한다. 추측하지 말고 반드시 호출한다.
    [입력] expression: 계산할 수식 문자열. 예: "12*(3+4)", "100/8"
    [출력] 계산 결과를 문자열로 반환한다. 예: "84"
    [주의] 파이썬 코드 실행 목적의 입력은 거부될 수 있다.
    """

from langchain_core.tools import tool

@tool
def calc_math(expression: str) -> str:
    """
    [언제 사용?] 수치/수학 계산이 필요하면 반드시 사용한다. 암산 금지.
    [입력] expression: 예 "12*(3+4)"
    [출력] 결과 문자열 예 "84"
    """
    return str(eval(expression))

@tool
def search_web(query: str, top_k: int = 5) -> str:
    """
    [언제 사용?] 최신 정보/외부 근거가 필요할 때 사용한다. 기억으로 단정 금지.
    [입력] query: 검색어, top_k: 상위 결과 수
    [출력] 상위 결과를 텍스트로 요약 반환
    """
    return f"(stub) query={query}, top_k={top_k}"