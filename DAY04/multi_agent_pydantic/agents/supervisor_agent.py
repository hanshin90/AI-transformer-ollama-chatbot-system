from __future__ import annotations
from langchain.agents import create_agent


# 관리자 AGENT  생성
# 작업 내용에 적합한 작업 AGENT에게 일 전달
# -----------------------------------------
def create_supervisor_agent(llm, tools):
    system_prompt = """너는 Supervisor Agent다.
- 사용자의 요청을 보고 '직접 답변'할지, 'Worker에게 위임'할지 결정한다.
- 계산/정확한 결과가 필요한 질문은 worker_dispatch 도구로 Worker에게 위임한다.
- 간단한 대화/설명은 직접 답해도 된다.
"""
    return create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt
    )
