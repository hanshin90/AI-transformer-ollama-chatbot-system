# ============================================
# langgraph_workflow_example.py
# ============================================
from langgraph.graph import StateGraph, END

# =========================
# State 정의 (dict 사용)
# =========================
# state = {
#   "input": str,
#   "plan": str,
#   "result": str,
#   "verified": bool
# }

# =========================
# Node 정의
# =========================

def planner_node(state: dict) -> dict:
    print(">>> Planner 실행")
    user_input = state["input"]
    plan = f"'{user_input}'에 대한 답변 생성"
    return {"plan": plan}


def worker_node(state: dict) -> dict:
    print(">>> Worker 실행")
    result = f"답변 결과: {state['plan']}"
    return {"result": result}


def verifier_node(state: dict) -> dict:
    print(">>> Verifier 실행")
    result = state.get("result", "")
    verified = len(result) > 10  # 단순 검증
    return {"verified": verified}


def fallback_node(state: dict) -> dict:
    print(">>> Fallback 실행")
    return {"result": "Fallback 답변 제공"}


# =========================
# Workflow(Graph) 구성
# =========================

def build_workflow():
    graph = StateGraph(dict)

    # 노드 등록
    graph.add_node("planner", planner_node)
    graph.add_node("worker", worker_node)
    graph.add_node("verifier", verifier_node)
    graph.add_node("fallback", fallback_node)

    # 진입점
    graph.set_entry_point("planner")

    # 기본 흐름
    graph.add_edge("planner", "worker")
    graph.add_edge("worker", "verifier")

    # 조건 분기
    def route_after_verify(state):
        if state.get("verified"):
            return "success"
        return "fail"

    graph.add_conditional_edges(
        "verifier",
        route_after_verify,
        {
            "success": END,
            "fail": "fallback",
        },
    )

    graph.add_edge("fallback", END)

    return graph.compile()


# =========================
# 실행
# =========================
if __name__ == "__main__":
    app = build_workflow()

    output = app.invoke({
        "input": "LangGraph Workflow란 무엇인가?"
    })

    print("\n [ 최종 결과 ]")
    print(output)