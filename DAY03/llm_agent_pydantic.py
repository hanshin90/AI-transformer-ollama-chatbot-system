# ==================================================================
# Agent + Tool 연동
# ==================================================================
# ==================================================================
# 모듈 로딩
# ==================================================================
from langchain_ollama import ChatOllama
from langchain.agents import create_agent

# 커스텀 사용자 정의 툴(전체 가져오기)
from ex_tools_multi_pydantic import *

# ==================================================================
# Agent AI : Prompt + 규칙
# ==================================================================
#[1] LLM 모델 인스턴스 생성
LLM_MODEL = "llama3.1:latest"

llm = ChatOllama(model=LLM_MODEL)

#[2] LLM 구동 규칙 설정
system_prompt = """
규칙:
- 계산이 필요하면 calculator 사용
- 정보 탐색이 필요하면 web_search 사용
- 추측하지 말고 Tool 결과 기반으로 답변
"""

#[3] Agent 생성
agent = create_agent(
    model=llm,
    tools=[calculator, web_search],
    system_prompt=system_prompt
)

#[4] Agent AI 질문 전달
result = agent.invoke({
    "messages": [("user", "12 * (3 + 4)는 얼마인가요?")]
})

print(result["messages"][-1].content)