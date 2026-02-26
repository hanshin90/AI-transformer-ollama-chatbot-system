## ==========================================================
##                Agent AI 서비스 
##   Agent를 생성하고, 사용자 질문을 넣어 실행(invoke)해서 
##   최종 답변을 출력하는 “실행용 엔트리 포인트” 파일
## ==========================================================
## -> ollama push qwen2.5:7b
## -> pip uninstall -y huggingface_hub transformers sentence-transformers
## -> pip install -U huggingface_hub transformers sentence-transformers
## ==========================================================
## -> Tool(=rag_search)을 준비해두고
## -> LLM(=ChatOllama)을 연결하고
## -> Agent를 만들고
## -> 한 번 실행해보는 파일
## ==========================================================
## 전체 Flow
## (1) Ollama LLM 준비 (ChatOllama)
## (2) Tool 준비 (rag_search)
## (3) system_prompt로 규칙 정의
## (4) create_agent로 Agent 생성
## (5) agent.invoke로 질문 실행
## (6) 출력
## ==========================================================
import os
import sys
import json

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)

from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from tools.rag_tool import rag_search

LLM_MODEL = "qwen2.5:7b"


## =========================================================
## 서비스 시작 함수
## =========================================================
def main():
    ## tool calling 지원 모델을 사용
    llm = ChatOllama(model=LLM_MODEL)

    ##- Agent 규칙(행동 지침)
    system_prompt = """
너는 사내 규정/문서 질의응답을 돕는 AI Agent다.

규칙:
- 사내 규정/기술문서 질문은 rag_search를 사용한다.
- 권한(role)에 맞는 문서만 검색한다.
- 추측하지 말고 Tool 결과(JSON)의 answer를 기반으로 사용자에게 설명한다.
""".strip()

    ## Agent 생성
    agent = create_agent(
        model=llm,
        tools=[rag_search],
        system_prompt=system_prompt
    )

    # 데모 질문 생성
    user_text = (
        "연차 사용 규정 알려줘. "
        "나는 employee(일반 직원)이고, 2024년 이후 문서 기준으로 bullet 형식으로 요약해줘."
    )

    ## 답변 생성
    result = agent.invoke({
        "messages": [("user", user_text)]
    })

    # 마지막 메시지 출력
    print(result["messages"][-1].content)

if __name__ == "__main__":
    main()
