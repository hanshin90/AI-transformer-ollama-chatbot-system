import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def worker_agent(state, tools):
    tool = tools[state["tool"]]
    result = tool.invoke(state["tool_args"])
    return {"result": result}
