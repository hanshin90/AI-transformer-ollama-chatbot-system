## ============================================================
##                      Supervisor Agent 생성   
## ============================================================
## -> 의사결정 프로세스 (Routing)기반으로 누구에게 일을 시킬지 결정 
## ============================================================
## -----------------------------------
## 모듈 로딩
## -----------------------------------
import json
import re
from typing import Literal
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage

LLM_MODEL = "qwen2.5:7b"

## -----------------------------------
## [1] 준비
## -----------------------------------
## -> [1-1] 의사결정 스키마 : Supervisor가 내릴 결정을 구조화 (Pydantic)
class RouterResponse(BaseModel):
    next_node: Literal["travel_expert", "weather_expert", "finish"] = Field(
        description="다음에 작업을 수행할 노드를 선택하세요."
    )
    reason: str = Field(description="이 노드를 선택한 이유")

## -> [1-2] Supervisor 전용 LLM 설정 (포맷을 JSON으로 강제)
llm = ChatOllama(model=LLM_MODEL, temperature=0, format="json")

SUPERVISOR_SYSTEM_PROMPT = (
    "당신은 여행 도우미 팀의 관리자입니다. 사용자의 질문을 분석하세요.\n"
    "1. 여행지 추천이 필요하면 'travel_expert'를 선택하세요.\n"
    "2. 날씨 정보가 필요하면 'weather_expert'를 선택하세요.\n"
    "3. 모든 정보(추천+날씨)가 대화 내역에 있다면 'finish'를 선택하세요.\n"
    "반드시 JSON 형식만 출력하세요. 예: {'next_node': 'travel_expert', 'reason': '...'}"
)


## -----------------------------------
## [2] Supervisor Agent 의사결정 루틴 함수
## -----------------------------------
## -> [1-3] 라우팅 함수 : 대화 내역에 따른 다음 단계를 결정
def get_supervisor_decision(state: list) -> RouterResponse:

    ## 현재까지의 대화 맥락을 기반으로 판단
    messages = [SystemMessage(content=SUPERVISOR_SYSTEM_PROMPT)] + state

    ## 구조화된 출력(Structured Output) 유도
    ## (Ollama의 경우 .with_structured_output이 모델별로 다를 수 있어 직접 파싱하거나 프롬프트로 유도)
    response = llm.invoke(messages)
    
    content = response.content.strip()
    
    try:
        # 정규표현식으로 JSON 부분만 추출 (불필요한 텍스트 방어)
        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        if json_match:
            content = json_match.group()
            
        data = json.loads(content)
        return RouterResponse(**data)
    
    except Exception as e:
        # 디버깅용: 실제 LLM이 뭐라고 했는지 출력
        print(f"--- [Debug] 파싱 실패. LLM 응답 원문: {content} ---")
        # 실패 시 질문에 '부산'이 있으면 우선 전문가에게 보냄 (fallback)
        return RouterResponse(next_node="travel_expert", reason="파싱 오류로 인한 기본값 실행")

