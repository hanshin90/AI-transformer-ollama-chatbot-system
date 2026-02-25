# ==================================================================
# Tool → Tool “체인”을 설계하고 실행 흐름을 구성
# ==================================================================
# -> Agent가 여러 Tool을 순차적으로 사용하도록 “작업 흐름”을 설계
# -> Tool 출력(JSON)을 다음 Tool 입력으로 연결하는 연습
# ==================================================================
# ==================================================================
# 모듈 로딩
# ==================================================================
from langchain_core.tools import tool

# ==================================================================
# Tool 생성
# -> Tool만 있고 체인이 없음
# ==================================================================
import json
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """특정 도시 날씨를 반환한다."""
    return json.dumps({"tool":"get_weather","ok":True,"data":{"city":city,"temp_c":22,"condition":"sunny"}}, ensure_ascii=False)

@tool
def c_to_f(celsius: float) -> str:
    """섭씨를 화씨로 변환한다."""
    f = celsius * 9/5 + 32
    return json.dumps({"tool":"c_to_f","ok":True,"data":{"celsius":celsius,"fahrenheit":f}}, ensure_ascii=False)

@tool
def summarize_tool_results(results_json_list: list[str]) -> str:
    """여러 Tool 결과를 한 문장으로 요약한다."""
    # TODO
    return ""



# ==================================================================
# Tool 개선
# -> 수동 체인 예시
# ==================================================================
import json

def run_chain(city: str) -> str:
    r1 = get_weather.invoke({"city": city})
    obj1 = json.loads(r1)

    if not obj1.get("ok"):
        return r1  # 실패 JSON 그대로 반환

    temp_c = obj1["data"]["temp_c"]

    r2 = c_to_f.invoke({"celsius": temp_c})
    obj2 = json.loads(r2)

    r3 = summarize_tool_results.invoke({"results_json_list": [r1, r2]})
    return r3

# 실행 예
print(run_chain("서울"))


# ==================================================================
# Tool 개선
# -> Agent 유도용 system_prompt 예시
# ==================================================================
# 규칙:
# - 날씨가 필요하면 get_weather 사용
# - 단위 변환이 필요하면 c_to_f 사용
# - 최종 답변은 summarize_tool_results 결과를 기반으로 한 문장으로 작성
# - 모든 Tool 출력은 JSON이므로 반드시 파싱해서 사용
# ==================================================================