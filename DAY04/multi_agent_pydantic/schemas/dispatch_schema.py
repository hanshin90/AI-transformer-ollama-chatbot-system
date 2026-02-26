## ==================================================================
##                  Tool 입력 데이터 검증 규칙 설정 
## 목적:Dispatcher Tool이 받을 입력의 규격 고정
## ==================================================================
## 입력 필드들 :
## -> worker_id / worker_name: 어느 워커가 처리할지
## -> task_type: 작업 종류 (예: calc, rag_search, summarize, web_search)
## -> payload: 작업에 필요한 입력값(질의, 수식, top_k 등)
## -> priority / deadline: 우선순위나 제한 시간(선택)
## -> trace_id / request_id: 로깅/성능 측정용 ID
## -> retry_policy: 재시도 정책(최대 횟수, backoff 등)
## ==================================================================

## ---------------------------------------
## 모듈 로딩
## ---------------------------------------
from pydantic import BaseModel, Field


## ---------------------------------------
## WorkerDispatch 툴의 입력 데이터 형식 정의
## ---------------------------------------
class WorkerDispatchInput(BaseModel):
    """Supervisor가 Worker에게 일을 위임할 때 사용하는 입력 스키마"""
    task: str = Field(..., description="Worker에게 보낼 작업/질문(자연어)")
