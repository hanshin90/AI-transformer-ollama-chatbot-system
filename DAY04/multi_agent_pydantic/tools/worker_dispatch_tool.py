## ==================================================================
##                 작업 라우터(Dispatcher) Tool 생성
## -> Planner가 만든 steps를 실행 가능한 호출로 변환하는 관문
## -> 규격대로 입력을 받아 실제 Worker/Tool 실행을 연결하는 실행부
## ==================================================================
## 목적: Planner/Controller가 만든 “작업(step)”을 받아서
##      해당 작업을 적절한 Worker(또는 Tool)에게 “라우팅/호출” 하는 Tool입니다.
##
## 보통 내부에서 하는 일:
## -> dispatch_schema로 입력 검증
## -> task_type 또는 worker_id에 따라 분기
## -> 실제 worker 함수/agent/tool 실행
## -> 결과를 표준 포맷으로 반환 (성공/실패/에러/latency 등)
## -> metrics/log 업데이트 (tool 호출 로그 기반 성능 측정에 핵심)
## ==================================================================

## ---------------------------------------
## 모듈 로딩
## ---------------------------------------
from __future__ import annotations
from langchain_core.tools import StructuredTool
from schemas.dispatch_schema import WorkerDispatchInput


## ---------------------------------------
## 해당 작업을 적절한 Worker(또는 Tool)에게 “라우팅/호출” 하는 Tool
## ---------------------------------------
def build_worker_dispatch_tool(worker_agent):
    """Worker Agent를 'Tool'처럼 감싸서 Supervisor가 호출할 수 있게 만듭니다."""

    def _dispatch(task: str) -> str:
        result = worker_agent.invoke({
            "messages": [("user", task)]
        })
        try:
            return result["messages"][-1].content
        except Exception:
            return str(result)

    return StructuredTool.from_function(
        name="worker_dispatch",
        description="복잡한 작업(계산/도구 사용)이 필요할 때 Worker Agent에게 위임합니다.",
        args_schema=WorkerDispatchInput,
        func=_dispatch,
    )