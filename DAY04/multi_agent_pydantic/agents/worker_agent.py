from __future__ import annotations
from langchain.agents import create_agent

#worker agent
#모델과 규칙이 적용된 worker agent 생성
def create_worker_agent(llm, tools):
    system_prompt = """너는 Worker Agent다.
- 실제 실행(계산 등)을 담당한다.
- 필요한 경우 도구를 사용해서 결과를 만든다.
- 가능한 한 짧고 정확하게 답한다.
"""
    #worker Agent 생성
    return create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt
    )
