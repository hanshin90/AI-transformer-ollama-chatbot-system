# ==================================================================
# Tool 생성
# ==================================================================

# ==============================
# 모듈 로딩
# =============================
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from ex_tools_multi_pydantic import *

# =============================
# Tool calling 지원 모델
# =============================
LLM_MODEL = "llama3.1"
llm = ChatOllama(model=LLM_MODEL)  # ← 이미 성공한 모델 사용


# =============================
# PromptTemplate, AgentExecutor X  ===> system_prompt OK
# =============================
system_prompt = """
너는 유능한 AI Agent다.

규칙:
- 계산이 필요하면 반드시 calculator를 사용한다.
- 정보 탐색이 필요하면 web_search를 사용한다.
- 추측하지 말고 Tool 결과를 기반으로 답변한다.
"""

# =============================
# Agent 생성 (Executor 개념은 내부로 흡수됨)
# =============================
agent = create_agent(
    model=llm,
    tools=[calculator, web_search],
    system_prompt=system_prompt
)

# =============================
# Tool 1: 계산
# ==============================
result1 = agent.invoke({
    "messages": [("user", "12 * (3 + 4)는 얼마인가요?")]
})
print("계산 결과:", result1["messages"][-1].content)


# =============================
# Tool 2: 검색
# =============================
result2 = agent.invoke({
    "messages": [("user", "인공지능이 뭐예요? 간단히 알려줘")]
})
print("검색 결과:", result2["messages"][-1].content)