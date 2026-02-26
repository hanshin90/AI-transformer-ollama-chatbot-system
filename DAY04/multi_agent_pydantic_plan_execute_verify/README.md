# Multi-Agent (Plan → Execute → Verify)
Pydantic + StructuredTool + LangGraph

## Agent 역할
- Planner Agent : 어떤 Tool을 쓸지 결정
- Worker Agent  : Tool 실행
- Verifier Agent: 결과 검증

## 실행
```bash
pip install -r requirements.txt
python agent/agent_run.py
```
