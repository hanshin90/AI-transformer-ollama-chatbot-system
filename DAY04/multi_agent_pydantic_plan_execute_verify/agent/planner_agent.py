import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def planner_agent(state):
    user_msg = state["messages"][-1][1]

    if any(op in user_msg for op in ["+", "-", "*", "/"]):
        return {"tool": "calculator", "tool_args": {"expression": user_msg}}

    return {"tool": "search", "tool_args": {"query": user_msg}}
