from langgraph.graph import StateGraph, END

# -------------------------
# Planner (steps 생성 / 재계획)
# -------------------------
def planner_node(state: dict) -> dict:
    user_input = state["messages"][-1][1]
    r = state.get("replan_count", 0)

    if r == 0:
        steps = [
            {"tool": "search", "args": {"query": user_input, "top_k": 2}},
        ]
    elif r == 1:
        steps = [
            {"tool": "search", "args": {"query": user_input, "top_k": 4}},
        ]
    else:
        steps = [
            {"tool": "search", "args": {"query": user_input, "top_k": 6}},
        ]

    print(f">>> Planner (replan={r}) → steps={steps}")
    return {"steps": steps}


# -------------------------
# Worker (steps 실행)
# -------------------------
def worker_node(state: dict) -> dict:
    outputs = []

    for step in state.get("steps", []):
        if step["tool"] == "search":
            q = step["args"]["query"]
            k = step["args"]["top_k"]
            # mock RAG 결과
            result = f"[RAG 결과 k={k}] {q}에 대한 규정 요약"
            outputs.append(result)

    final_result = outputs[-1] if outputs else ""
    print(">>> Worker result:", final_result)
    return {"result": final_result}


# -------------------------
# Verifier (검증)
# -------------------------
def verifier_node(state: dict) -> dict:
    result = state.get("result", "")
    verified = len(result) >= 30
    reason = "ok" if verified else "too_short"

    print(f">>> Verifier → {verified} ({reason})")
    return {"verified": verified, "verify_reason": reason}


# -------------------------
# Routing (Replan / 종료)
# -------------------------
def route_after_verify(state: dict) -> str:
    if state.get("verified"):
        return "finalize"

    state["replan_count"] = state.get("replan_count", 0) + 1
    if state["replan_count"] > state.get("max_replans", 2):
        return "fallback"

    return "planner"


# -------------------------
# Final / Fallback
# -------------------------
def finalize_node(state: dict) -> dict:
    return {"final_answer": state.get("result")}


def fallback_node(state: dict) -> dict:
    return {"final_answer": "!!! 재계획 한계를 초과했습니다. 추가 질문이 필요합니다."}


# -------------------------
# Graph 구성
# -------------------------
def build_graph():
    g = StateGraph(dict)

    g.add_node("planner", planner_node)
    g.add_node("worker", worker_node)
    g.add_node("verifier", verifier_node)
    g.add_node("finalize", finalize_node)
    g.add_node("fallback", fallback_node)

    g.set_entry_point("planner")
    g.add_edge("planner", "worker")
    g.add_edge("worker", "verifier")

    g.add_conditional_edges(
        "verifier",
        route_after_verify,
        {
            "planner": "planner",      ## Replan
            "finalize": "finalize",
            "fallback": "fallback",
        },
    )

    g.add_edge("finalize", END)
    g.add_edge("fallback", END)

    return g.compile()


# -------------------------
# 실행
# -------------------------
if __name__ == "__main__":
    app = build_graph()

    out = app.invoke({
        "messages": [("user", "2024년 연차 규정 요약해줘")],
        "replan_count": 0,
        "max_replans": 2,
    })

    print("\n ===> FINAL ANSWER")
    print(out["final_answer"])