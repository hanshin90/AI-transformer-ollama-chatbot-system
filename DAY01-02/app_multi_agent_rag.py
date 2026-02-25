# =========================================================
# Multi-Agent RAG 예제 (Search + Analyzer + Writer)
# ---------------------------------------------------------
# 구성:
#  - SearchAgent   : RAG 검색 전용
#  - AnalyzerAgent : 근거 분석/요약
#  - WriterAgent   : 최종 답변 작성
#
# 요구사항:
#  1) Ollama 설치
#  2) ollama pull llama3.1:latest
#  3) ollama pull nomic-embed-text
#  4) pip install -U langchain-ollama langchain-community langchain-text-splitters chromadb
#
# 실행:
#  python app_multi_agent_rag.py
# =========================================================

import os
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

# =========================
# 경로 설정
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
VEC_DIR = os.path.join(BASE_DIR, ".chroma_docs")

# =========================
# VectorStore (RAG)
# =========================
def build_vectorstore():
    docs = []
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

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    texts, metas = [], []

    for d in docs:
        chunks = splitter.split_text(d["text"])
        for i, ch in enumerate(chunks):
            texts.append(ch)
            metas.append({"source": d["source"], "chunk": i})

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

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

@tool
def search_docs(query: str, k: int = 4) -> str:
    """질문과 관련된 문서 조각을 검색한다."""
    global _VECTORSTORE
    if _VECTORSTORE is None:
        _VECTORSTORE = build_vectorstore()

    results = _VECTORSTORE.similarity_search(query, k=k)
    if not results:
        return "관련 문서를 찾지 못했습니다."

    out = []
    for r in results:
        src = r.metadata.get("source", "unknown")
        ck = r.metadata.get("chunk", "?")
        snippet = r.page_content[:300].replace("\n", " ")
        out.append(f"- [source={src}, chunk={ck}] {snippet} ...")

    return "\n".join(out)


# =========================
# LLM 공통 설정
# =========================
llm = ChatOllama(
    model="llama3.1:latest",
    temperature=0,
    streaming=False
)

# =========================
# Agent 1: Search Agent
# =========================
search_agent = create_react_agent(
    model=llm,
    tools=[search_docs],
    prompt=(
        "너는 문서 검색 Agent이다.\n"
        "질문에 대해 관련 문서 조각만 검색하라.\n"
        "해석이나 결론은 작성하지 말고 검색 결과만 반환하라."
    )
)

# =========================
# Agent 2: Analyzer Agent
# =========================
analyzer_agent = create_react_agent(
    model=llm,
    tools=[],
    prompt=(
        "너는 분석 Agent이다.\n"
        "검색된 문서 조각을 근거로 핵심만 요약하라.\n"
        "중복을 제거하고 논리적으로 정리하라."
    )
)

# =========================
# Agent 3: Writer Agent
# =========================
writer_agent = create_react_agent(
    model=llm,
    tools=[],
    prompt=(
        "너는 최종 답변 작성 Agent이다.\n"
        "분석 결과를 바탕으로 사용자에게 제공할 답변을 작성하라.\n"
        "출력 형식:\n"
        "- 참고 문서\n"
        "- 핵심 요약\n"
        "- 결론"
    )
)


# =========================
# Multi-Agent Orchestration
# =========================
def multi_agent_answer(question: str) -> str:

    search_result = search_agent.invoke({
        "messages": [HumanMessage(content=question)]
    })["messages"][-1].content

    analysis = analyzer_agent.invoke({
        "messages": [HumanMessage(content=search_result)]
    })["messages"][-1].content

    final_answer = writer_agent.invoke({
        "messages": [HumanMessage(content=analysis)]
    })["messages"][-1].content

    return final_answer


# =========================
# CLI 실행
# =========================
def run_cli():
    print("\nMulti-Agent RAG 시스템")
    print(f"- docs 경로: {DOCS_DIR}")
    print("종료: exit\n")

    while True:
        q = input("Q> ").strip()
        if not q:
            continue
        if q.lower() in ("exit", "quit"):
            break

        answer = multi_agent_answer(q)
        print("\n" + "=" * 70)
        print(answer)
        print("=" * 70 + "\n")


if __name__ == "__main__":
    run_cli()
