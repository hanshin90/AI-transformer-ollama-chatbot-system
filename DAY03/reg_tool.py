## =========================================================
## RAG Tool (Vector DB 실제 사용)
## =========================================================
import json
from langchain_core.tools import StructuredTool
from rag_schema import RAGQueryInput
from vector_store import load_vector_store

vector_db = load_vector_store()

def _rag_search(
    query: str,
    document_types=None,
    after_year=None,
    top_k=3,
    answer_style="brief"
) -> str:
    # 메타데이터 필터 구성
    filters = {}
    if document_types:
        filters["doc_type"] = {"$in": document_types}
    if after_year:
        filters["year"] = {"$gte": after_year}

    docs = vector_db.similarity_search(
        query,
        k=top_k,
        filter=filters if filters else None
    )

    context = "\n".join([d.page_content for d in docs])

    answer = f"[{answer_style.upper()}]\n{context[:500]}"

    return json.dumps({
        "query": query,
        "filters": filters,
        "answer": answer
    }, ensure_ascii=False)

rag_search = StructuredTool.from_function(
    func=_rag_search,
    name="rag_search",
    description="사내 문서 기반 질문에 답변할 때 사용하는 RAG 검색 도구",
    args_schema=RAGQueryInput
)