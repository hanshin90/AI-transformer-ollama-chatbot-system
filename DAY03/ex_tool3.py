# ==================================================================
# Tool 결과(JSON)를 기반으로 “요약 Tool” 생성
# ==================================================================
# ==================================================================
# 모듈 로딩
# ==================================================================
from langchain_core.tools import tool

# ==================================================================
# Tool 생성
# -> Tool들이 JSON 문자열로 결과를 반환한다고 가정
# ==================================================================
import json
from langchain_core.tools import tool

@tool
def summarize_tool_results(results_json_list: list[str]) -> str:
    """
    [언제 사용?] 여러 Tool의 JSON 결과를 한 번에 요약해야 할 때 사용한다.
    [입력] results_json_list: Tool들이 반환한 JSON 문자열 리스트
    [출력] 요약 결과 JSON 문자열
    """
    # TODO: 구현
    return ""


# ==================================================================
# Tool 개선
# -> JSON 파싱 실패를 안전하게 처리하는가
# -> Tool별 핵심 필드를 일관되게 요약하는가
# -> 출력이 JSON 문자열로 표준화돼 있는가
# ==================================================================
import json
from langchain_core.tools import tool

@tool
def summarize_tool_results(results_json_list: list[str]) -> str:
    """
    [언제 사용?] 여러 Tool의 JSON 결과를 한 번에 요약해야 할 때 사용한다.
    [입력] results_json_list: Tool들이 반환한 JSON 문자열 리스트
    [출력] {"tool":"summarize_tool_results","summary":"...","items":[...],"skipped":[...]}
    """
    items = []
    skipped = []

    for i, s in enumerate(results_json_list):
        try:
            obj = json.loads(s)
            tool_name = obj.get("tool", "unknown")

            # Tool별 핵심 필드 추출 예시
            if tool_name == "calc":
                items.append({"tool": tool_name, "result": obj.get("result")})
            elif tool_name == "get_time":
                items.append({"tool": tool_name, "time": obj.get("time")})
            elif tool_name == "get_weather":
                items.append({
                    "tool": tool_name,
                    "city": obj.get("city"),
                    "temp": obj.get("temp"),
                    "condition": obj.get("condition")
                })
            else:
                items.append({"tool": tool_name, "raw_keys": list(obj.keys())})

        except Exception as e:
            skipped.append({"index": i, "error": str(e)})

    # 사람이 읽기 쉬운 summary 텍스트(선택)
    summary_lines = []
    for it in items:
        if it["tool"] == "calc":
            summary_lines.append(f"계산 결과: {it.get('result')}")
        elif it["tool"] == "get_time":
            summary_lines.append(f"현재 시간: {it.get('time')}")
        elif it["tool"] == "get_weather":
            summary_lines.append(f"{it.get('city')} 날씨: {it.get('temp')}°C, {it.get('condition')}")
        else:
            summary_lines.append(f"{it['tool']} 결과 요약")

    out = {
        "tool": "summarize_tool_results",
        "summary": " / ".join(summary_lines) if summary_lines else "",
        "items": items,
        "skipped": skipped
    }
    return json.dumps(out, ensure_ascii=False)