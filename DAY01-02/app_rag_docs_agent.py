# =========================================================
# 실무형 RAG 문서 검색 AI Agent (CLI)
# ---------------------------------------------------------
# 요구사항:
#   - Ollama 모델들 설치 
#   - windows cmd 명령어 프롬프트에서 설치
#   - ollama pull llama3.1:latest
#   - ollama pull nomic-embed-text
#   - pip install -U langchain-ollama langchain-community langchain-text-splitters chromadb
#
# 실행:
#   python app_rag_docs_agent.py
# =========================================================

import os
from typing import Optional

from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

# =========================
# 설정
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
VEC_DIR = os.path.join(BASE_DIR, ".chroma_docs")

MAX_CHARS_PER_READ = 6000

print(f"BASE_DIR : {BASE_DIR}")
print(f"DOCS_DIR : {DOCS_DIR}")
print(f"VEC_DIR  : {VEC_DIR}")

# =========================
# Tools: 문서 목록
# =========================
@tool
def list_docs() -> str:
    """docs 폴더에 있는 문서 파일 목록을 줄바꿈으로 반환한다."""
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
# Tools: [1]문서 부분 읽기
# =========================
@tool
def read_doc(filename: str, start: int = 0, max_chars: int = MAX_CHARS_PER_READ) -> str:
    """
    지정한 문서 파일의 내용을 부분적으로 반환한다.
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


# =========================
# RAG: VectorStore 구축
# =========================
def build_vectorstore():
    docs = []

    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR, exist_ok=True)

    for fn in os.listdir(DOCS_DIR):
        path = os.path.join(DOCS_DIR, fn)
        if not os.path.isfile(path):
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            docs.append({"text": text, "source": fn})
        except Exception:
            pass
    ##파일 전체 데이터를 900크기로 분리 => 단, 오버랩 150
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150
    )

    ## [2] 데이터 전처리
    ## texts : 실제 900크기로 (150이 오버랩된 상태) 데이터만 저장
    ## metas : 데이터에 대한 정보 원본 위치와 인덱스 저장
    texts, metas = [], []
    for d in docs:
        chunks = splitter.split_text(d["text"])
        for i, ch in enumerate(chunks):
            texts.append(ch)
            metas.append({"source": d["source"], "chunk": i})

    ##---------------------------------------------
    ## [3] 임베딩 진행 + 벡터 데이터베이스 저장
    ##---------------------------------------------
    ## 임베딩 모델 객체 생성
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    ## 실수화 즉, 벡터화 된 데이터 저장용 Database 생성
    vectordb = Chroma(
        collection_name="docs",
        embedding_function=embeddings,
        persist_directory=VEC_DIR,
    )

    if vectordb._collection.count() == 0 and texts:
        vectordb.add_texts(texts=texts, metadatas=metas)
        vectordb.persist()

    return vectordb


_VECTORSTORE = None


# =========================
# Tools: RAG 검색
# =========================
@tool
def search_docs(query: str, k: int = 4) -> str:
    """질문(query)과 의미적으로 유사한 문서 조각을 검색한다."""

    ## 벡터 데이터베이스가 없으면 생성하기
    global _VECTORSTORE
    if _VECTORSTORE is None:
        _VECTORSTORE = build_vectorstore()

    ## 질문과 유사한 데이터 검색 후 유사성이 높은 상위 K개 가져오기
    results = _VECTORSTORE.similarity_search(query, k=k)
    if not results:
        return "관련 문서를 찾지 못했습니다."

    ## 질문에 대한 근거 자료 생성
    out = []
    for r in results:
        src = r.metadata.get("source", "unknown")
        ck = r.metadata.get("chunk", "?")
        snippet = r.page_content[:300].replace("\n", " ")
        out.append(f"- [source={src}, chunk={ck}] {snippet} ...")

    return "\n".join(out)


# =========================
# Agent 구성
# =========================
def build_agent():
    ## LLM에 역할 및 agent 동작 규칙 지정 프롬프트
    llm = ChatOllama(
        model="llama3.1:latest",
        temperature=0,
        streaming=False
    )

    system_prompt = (
        "너는 '실무형 사내 문서 RAG Agent'이다.\n"
        "목표: docs 폴더의 문서를 근거로 질문에 답하라.\n\n"
        "규칙:\n"
        "1) 내용 검색이 필요하면 search_docs(query)를 먼저 사용한다.\n"
        "2) 파일 목록이 필요하면 list_docs를 사용한다.\n"
        "3) 원문 확인이 필요하면 read_doc(filename, start)를 사용한다.\n"
        "4) 내부 추론 과정은 출력하지 말고 최종 답변만 제공한다.\n\n"
        "출력 형식:\n"
        "- 참고 문서\n"
        "- 핵심 요약 (3~7개)\n"
        "- 결론\n"
        "언어: 한국어\n"
    )

    ## 도구 + 검색 기반 agent 생성(RAG)
    agent = create_react_agent(
        model=llm,
        tools=[search_docs, list_docs, read_doc],
        prompt=system_prompt
    )
    return agent


# =========================
# CLI 실행
# =========================
def run_cli():
    agent = build_agent()
    print("\n실무형 RAG 문서 검색 Agent (LangGraph + Ollama llama3.1)")
    print(f"- docs 경로: {DOCS_DIR}")
    print("종료: exit\n")

    while True:
        q = input("Q> ").strip()
        if not q:
            continue
        if q.lower() in ("exit", "quit"):
            break

        result = agent.invoke({"messages": [HumanMessage(content=q)]})
        print("\n" + "=" * 70)
        print(result["messages"][-1].content)
        print("=" * 70 + "\n")


if __name__ == "__main__":
    run_cli()
