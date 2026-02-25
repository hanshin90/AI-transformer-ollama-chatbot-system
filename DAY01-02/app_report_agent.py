# =========================================================
# 보고서 작성 Agent (CLI)
# =========================================================
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

llm = ChatOllama(model="llama3.1:latest", temperature=0)

REPORT_PROMPT = """
너는 '보고서 작성 Agent'이다.
공식적이고 구조화된 보고서를 작성하라.

보고서 구조:
1. 개요
2. 배경
3. 주요 내용
4. 분석 및 시사점
5. 결론
"""

agent = create_react_agent(model=llm, tools=[], prompt=REPORT_PROMPT)

def run():
    print("보고서 작성 Agent (exit 입력 시 종료)")
    while True:
        topic = input("보고서 주제: ")
        if topic.lower() == "exit":
            break
        result = agent.invoke({
            "messages": [HumanMessage(content=f"주제: {topic}")]
        })
        print("\n" + result["messages"][-1].content + "\n")

if __name__ == "__main__":
    run()
