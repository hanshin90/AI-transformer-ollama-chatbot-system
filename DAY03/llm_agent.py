# ==================================================================
# LLM + Agent 연결
# ---------------------------------------------------------
# 요구사항:
#   - pip install -U langgraph langchain langchain-core langchain-community
#   - pip install -U langchain-ollama
#
# 실행:
#   python tools.py
# ==================================================================

# ===================================
# 모듈 로딩
# ===================================
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langchain.agents import create_agent

from tools import calculator


# ===================================
# 전역변수
# ===================================
LLM_NAME = "llama3.1:8b"

import langgraph, langchain
from importlib.metadata import version

LANGGRAPH_V = version("langgraph")
print("langgraph version :", version("langgraph"))
print("langchain version :", version("langchain"))
# print(f"langgraph.__version__ : {langgraph.__version__}")
# print(f"langchain.__version__ : {langchain.__version__}")


# ===================================
# ReAct Agent 전용 Prompt 핵심 규약
# ===================================
prompt = PromptTemplate.from_template("""
You are a helpful AI agent.

You have access to the following tools:
{tools}

Use the following format:

Question: {input}
Thought: you should think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
Final Answer: the final answer

Begin!

Question: {input}
{agent_scratchpad}
""")


# ===================================
# LLM 생성 (Ollama)
# ===================================
llm = ChatOllama(model=LLM_NAME)


# ===================================
# Agent 생성
# ===================================
print(f"LANGGRAPH_V[0]={LANGGRAPH_V[0]}")

if LANGGRAPH_V[0] == '0':
    agent = create_react_agent(
        model=llm,          # ← 중요: llm 아님, model 임
        tools=[calculator],
    )
else:
    agent = create_agent(
        model=llm,
        tools=[calculator],
        system_prompt=prompt
    )



# ===================================
# 실행
# ===================================
result = agent.invoke({
    "messages": [
        ("user", "12 * (3 + 4)는 얼마인가요? 계산기 도구를 사용해서 답해줘.")
    ]
})

# LangGraph는 messages로 결과를 반환
print("\n최종 출력:")
print(result["messages"][-1].content)