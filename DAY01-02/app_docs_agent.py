# ===================================================================
#  LLM이 스스로 판단하여 도구(tool)를 호출하며 문제를 해결하는 
#                도구 기반 AI Agent(ReAct Agent)
# -> LLM이 스스로 판단                          OK
# -> 외부 행동(도구)을 실행                      Ok
# -> 목표 달성을 위한 반복적 추론 흐름             OK
# ===================================================================
#  로컬 PC의 docs 폴더 안에 있는 문서들을 필요할 때만 찾아 읽어서 
#  질문에 답하는 CLI(터미널)용 에이전트를 만드는 스크립트
# ===================================================================
# 1) 목적
#   사용자가 질문하면,
#   에이전트가 docs 폴더에 어떤 파일이 있는지 확인하고(list_docs)
#   답변 근거가 필요하면 해당 파일 내용을 일부 읽어서(read_doc)
#   근거 기반 요약/결론 형태로 답변하게 만드는 것이 목적 

#   즉, “문서 내용을 전부 LLM에 넣는 방식”이 아니라
#   도구(tool)를 통해 문서를 ‘탐색’하고 ‘부분 읽기’하는 문서 탐색 에이전트
#
# 2) 주요 기능
#    A. 폴더 경로 자동 설정
#    B. Tool 1: 문서 목록 조회
#    C. Tool 2: 문서 내용 읽기
#    D. LangGraph ReAct Agent 구성
#    E. CLI 실행 루프
# ===================================================================

# =========================
# 관련 모듈 로딩
# =========================
import os
from typing import Optional

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

# =========================
# 설정 : 폴더 경로 자동 설정
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "docs")

# 문서 한 번에 너무 길게 넣지 않도록 제한(필요시 조절)
MAX_CHARS_PER_READ = 6000

print(f'BASE_DIR : { BASE_DIR}')
print(f'DOCS_DIR : { DOCS_DIR}')

# =========================
# Tools : 문서 목록 조회
# =========================
@tool
def list_docs() -> str:
    """docs 폴더에 있는 문서 파일 목록을 줄바꿈으로 반환"""
    try:
        files = sorted(
            f for f in os.listdir(DOCS_DIR)
            if os.path.isfile(os.path.join(DOCS_DIR, f))
        )
        if not files:
            return "docs 폴더에 파일이 없습니다."
        return "\n".join(files)
    except Exception as e:
        return f"목록 조회 실패: {e}"

# =========================
# Tools : 문서 내용 읽기
# =========================
@tool
def read_doc(filename: str, start: int = 0, max_chars: int = MAX_CHARS_PER_READ) -> str:
    """
    지정한 문서 파일의 내용을 반환한다.
    - filename: list_docs에 있는 파일명
    - start: 읽기 시작 위치(문자 인덱스)
    - max_chars: 최대 읽기 문자 수
    """
    path = os.path.join(DOCS_DIR, filename)
    if not os.path.exists(path):
        return "문서가 존재하지 않습니다. list_docs로 파일명을 확인하세요."

    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        end = min(len(text), start + max_chars)
        chunk = text[start:end]
        meta = f"[FILE={filename}] [CHARS={start}:{end}/{len(text)}]"
        return meta + "\n" + chunk
    except Exception as e:
        return f"문서 읽기 실패: {e}"


# =======================================
# Agent 구성 
# cmd => ollama pull llama3.1
# =======================================
def build_agent():
    #LLM => 핵심 요소 : 분석 + 계획 
    llm = ChatOllama(model="llama3.1", temperature=0,  streaming=False)
    #LLM을 판단해서 적합한 Tool을 선택할 수 있는 프롬프 
    system_prompt = (
        "너는 '문서 구조 탐색 Agent'이다.\n"
        "목표: 사용자의 질문에 답하기 위해 docs 폴더의 문서를 찾아 읽고 근거 기반으로 답하라.\n\n"
        "규칙:\n"
        "1) 어떤 문서가 있는지 모르면 list_docs를 호출한다.\n"
        "2) 답변에 필요한 근거가 있으면 read_doc(filename)를 호출해서 내용을 확인한다.\n"
        "3) 문서가 길면 start를 늘려 여러 번 나누어 읽을 수 있다.\n"
        "4) 최종 답변 형식:\n"
        "   - 참고 문서: 파일명 리스트\n"
        "   - 핵심 요약: 3~7개 불릿\n"
        "   - 결론: 질문에 대한 직접 답변\n"
        "5) 근거가 부족하면 '문서에서 확인 불가'를 명시하고, 어떤 문서가 더 필요할지 제안한다.\n"
        "6) 기본 출력 언어는 한국어로 한다.\n"
    )
    ##Agent 생성 : 도구 기반 AI agent
    ## -> LLM, Tool, Prompt
    agent = create_react_agent(
        model=llm,
        tools=[list_docs, read_doc],
        prompt=system_prompt
    )
    return agent

# =======================================
# CLI 실행 루프
# =======================================
def run_cli():
    agent = build_agent()
    print("문서 구조 탐색 Agent (LangGraph + Ollama llama3)")
    print(f"- docs 경로: {DOCS_DIR}")
    print("종료: exit\n")

    
    print("질문하세요.\n")
    while True:
        q = input("Q> ").strip()
        if not q:
            continue
        if q.lower() in ("exit", "quit","q","x"):
            print("사용자 요청으로 종료합니다.\n")
            print("=====================")
            break

        result = agent.invoke({"messages": [HumanMessage(content=q)]})
        print("\n" + "=" * 70)
        print(result["messages"][-1].content)
        print("=" * 70 + "\n")


if __name__ == "__main__":
    run_cli()