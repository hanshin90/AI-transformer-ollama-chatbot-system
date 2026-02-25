# ==================================================================
# Tool 출력 형식을 통일하여 Agent 체인을 안정화
# ==================================================================
# ==================================================================
# 모듈 로딩
# ==================================================================
from langchain_core.tools import tool

# ==================================================================
# Tool 생성
# -> 각각 다른 출력 형식을 사용
# -> 출력 타입이 int, str, dict로 제각각
# -> Agent가 다음 행동을 결정하기 어려움
# -> Tool 체인 연결 시 오류 가능성 ↑
# ==================================================================
@tool
def calc(expression: str):
    return eval(expression)

@tool
def get_time() -> str:
    return "현재 시간은 14시 30분입니다."

@tool
def get_weather(city: str):
    return {
        "city": city,
        "temp": 22,
        "condition": "sunny"
    }


# ==================================================================
# Tool 개선
# -> 모든 Tool 출력 형식을 통일
# -> JSON 문자열(str)로 반환
# -> key 이름은 일관성 유지
# ==================================================================
import json
from langchain_core.tools import tool

@tool
def calc(expression: str) -> str:
    """
    [언제 사용?] 수학 계산이 필요할 때 사용
    """
    result = eval(expression)
    return json.dumps({
        "tool": "calc",
        "result": result
    })

@tool
def get_time() -> str:
    """
    [언제 사용?] 현재 시간을 정확히 알아야 할 때 사용
    """
    return json.dumps({
        "tool": "get_time",
        "time": "14:30"
    })

@tool
def get_weather(city: str) -> str:
    """
    [언제 사용?] 특정 도시의 날씨 정보를 확인할 때 사용
    """
    return json.dumps({
        "tool": "get_weather",
        "city": city,
        "temp": 22,
        "condition": "sunny"
    })

