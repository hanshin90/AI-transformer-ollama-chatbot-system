from langgraph.graph import StateGraph, END
from agent.planner_agent import planner_agent
from agent.worker_agent import worker_agent
from agent.verifier_agent import verifier_agent
from tools.calc_tool import calc_tool
from tools.search_tool import search_tool

#agent system 작업 설계도 생성
def build_graph():

    #도구
    tools = {
        "calculator": calc_tool,
        "search": search_tool,
    }

    #작업흐름설정
    g = StateGraph(dict)
    g.add_node("planner", planner_agent)
    g.add_node("worker", lambda s: worker_agent(s, tools))
    g.add_node("verifier", verifier_agent)

    g.set_entry_point("planner")
    g.add_edge("planner", "worker")
    g.add_edge("worker", "verifier")
    g.add_edge("verifier", END)

    return g.compile()
