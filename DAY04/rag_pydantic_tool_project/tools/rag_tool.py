## ==========================================================
##       RAG기반 Tool 정의 : Agent가 호출하는 RAG 전용 Tool
## ==========================================================
## - Pydantic 입력 스키마를 받아
## - 권한·필터를 적용해 Vector DB에서 문서를 검색
## - RAG 결과를 JSON으로 반환하는 Tool을 정의
## ※ 질문 + 조건 + 권한 구조적으로 처리
## ==========================================================
## Agent
##  → rag_search Tool 호출
##     → Pydantic 스키마로 입력 검증
##     → 권한(role) 기반 문서 접근 제한
##     → Vector DB(Chroma) 유사도 검색
##     → 결과를 JSON으로 반환
##     → Agent가 JSON을 읽어 사용자에게 설명
## ==========================================================

## ==========================================
## 모듈 로딩
## ==========================================
## - 모듈 로딩 & 경로 설정
import os
import sys
import json
from typing import Optional, List

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)

## - Tool & 스키마 import
from langchain_core.tools import StructuredTool
from schema.rag_schema import RAGQueryInput
from ingest.vector_store import load_vector_store


## ==========================================
## 실제 RAG 로직 함수
## ==========================================
## ------------------------------------------
## - Pydantic Schema와 시그니처가 1:1 대응
## - 이 함수는 직접 호출하지 않음
## - 항상 StructuredTool을 통해서만 호출
## ------------------------------------------
def _rag_search(
    query: str,
    role: str,
    document_types: Optional[List[str]] = None,
    after_year: Optional[int] = None,
    top_k: int = 3,
    answer_style: str = "brief",
) -> str:
    """실무형 RAG 검색(예제)

    - 권한(role)에 따라 접근 가능한 문서 유형을 제한
    - 문서 유형/연도 필터를 메타데이터로 적용
    - 반환은 JSON 문자열(관찰/디버깅 용이)
    """
    ## -------------------------------------
    ##-> Vector DB 로딩
    ## -------------------------------------
    persist_dir = os.path.join(ROOT, "chroma_db")
    vector_db = load_vector_store(persist_dir=persist_dir)

     ## -------------------------------------
    ## -> 권한 기반 접근 제어
    ## -> RAG에서 가장 중요한 통제 지점
    ## -------------------------------------
    if role == "employee":
        allowed_types = ["HR_POLICY"]
    elif role == "manager":
        allowed_types = ["HR_POLICY", "GENERAL_GUIDE"]
    else:  # admin
        allowed_types = None  # 전체 허용

    ## -------------------------------------
    ## -> 메타데이터 필터 구성 
    ##    RAG 품질의 핵심 = 필터 설계
    ## -> Chroma의 where 필터는 항상 논리 연산자 하나로 시작해야 한다!!
    ## -> 조건이 2개 이상이면 반드시 $and로 묶어야 함!!
    ## -------------------------------------
    where_clauses = []

    # 권한 제한 우선 적용
    if allowed_types:
        where_clauses.append({
            "doc_type": {"$in": allowed_types}
        })

    # 사용자가 document_types를 지정하면 더 좁힘 (단, allowed_types 밖이면 결과 0이 나올 수 있음)
    if document_types:
        where_clauses.append({
            "doc_type": {"$in": document_types}
        })

    if after_year:
        where_clauses.append({
            "year": {"$gte": after_year}
        })

    filters = {"$and": where_clauses} if where_clauses else None

    ## -------------------------------------
    ## -> Vector DB 검색 + 메타데이터 필터 : 유사도 검색
    ## -------------------------------------
    docs = vector_db.similarity_search(
        query,
        k=top_k,
        filter=filters if filters else None
    )

    ## -------------------------------------
    ## 컨텍스트 구성
    ## - 검색된 문서 텍스트를 하나로 결합
    ## - 토큰 제한/ 중복 제거 /중요 문장 추출 등 추가 가능
    ## -------------------------------------
    context = "\n\n".join([d.page_content for d in docs])


    ## -------------------------------------
    ## 스타일에 따른 출력 가이드
    ## - 출력 형태까지 제어
    ## -> 실무 : 결과를 다시 LLM에게 요약시키는 구조로 확장
    ## -------------------------------------
    if answer_style == "bullet":
        answer = "\n".join([f"- {line.strip()}" for line in context.splitlines() if line.strip()])[:1200]
    elif answer_style == "detailed":
        answer = context[:1200]
    else:
        answer = context[:600]

    ## -------------------------------------
    ## JSON 반환 : Tool은 항상 JSON 반환이 정석
    ## -> Agent가 Observation으로 안정적으로 해석
    ## -> 디버깅/로그/평가에 매우 유리
    ## -> 실패 시에도 동일한 포맷 유지 가능
    ## -------------------------------------
    return json.dumps({
        "tool": "rag_search",
        "ok": True,
        "data": {
            "query": query,
            "role": role,
            "filters": filters,
            "top_k": top_k,
            "answer_style": answer_style,
            "answer": answer,
            "retrieved": [{"metadata": d.metadata} for d in docs],
        }
    }, ensure_ascii=False)


## ------------------------------------------
## Tool 등록
## ------------------------------------------
##  입력을 구조로 분리하고 / 검증/ Vector DB 필터까지 
##  정확히 연결된 StructuredTool
## _rag_search → Agent가 호출 가능한 Tool로 변환
## args_schema → 입력 검증 + 설명 제공
## description → Agent가 언제 이 Tool을 써야 하는지 판단
## ------------------------------------------
rag_search = StructuredTool.from_function(
    func=_rag_search,
    name="rag_search",
    description="사내 문서 기반 질문에 답변할 때 사용하는 RAG 검색 도구 (권한/필터 지원)",
    args_schema=RAGQueryInput
)
