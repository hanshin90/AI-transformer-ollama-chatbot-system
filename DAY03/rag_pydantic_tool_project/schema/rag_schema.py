## ==========================================================
##       RAG기반 Tool 정의 : Agent가 호출하는 RAG 전용 Tool
##   RAG 품질 정하는 입력 설계도. 검색 성능보다 먼저 스키마 설계!!
## ==========================================================
## - RAG Tool에 들어갈 입력을 “질문 + 조건 + 권한”으로 구조화
## - Agent가 Tool을 정확히 호출하도록 만드는 입력 계약서(스키마) 파일
## ※ 질문 + 조건 + 권한 구조적으로 처리
## ==========================================================
## -> 사용자의 자연어 요청을 그대로 쓰지 않고
## -> 검색 조건을 필드로 분리해서
## -> Vector DB 필터와 답변 스타일까지 제어
## ==========================================================
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class RAGQueryInput(BaseModel):
    query: str = Field(description="사용자의 질문")

    role: Literal["employee", "manager", "admin"] = Field(
        description="사용자 권한 (employee=직원, manager=관리자, admin=전체)"
    )

    document_types: Optional[List[Literal[
        "HR_POLICY",
        "TECH_DOC",
        "SECURITY_RULE",
        "GENERAL_GUIDE"
    ]]] = Field(
        default=None,
        description="검색할 문서 유형 목록. 지정하지 않으면 권한 범위 내에서 전체 검색"
    )

    after_year: Optional[int] = Field(
        default=None,
        ge=2000,
        description="이 연도 이후에 작성된 문서만 검색"
    )

    top_k: int = Field(
        default=3,
        ge=1,
        le=10,
        description="검색할 문서 개수 (1~10)"
    )

    ## -> 응답 형식 
    answer_style: Literal["brief", "detailed", "bullet"] = Field(
        default="brief",
        description="답변 스타일: brief(요약), detailed(상세), bullet(항목형)"
    )
