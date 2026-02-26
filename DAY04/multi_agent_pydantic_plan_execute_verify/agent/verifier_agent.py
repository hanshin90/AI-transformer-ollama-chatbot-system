import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def verifier_agent(state):
    result = state.get("result")
    if result is None or len(str(result)) < 3:
        return {"verified": False}
    return {"verified": True}
