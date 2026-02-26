## ============================================================
##                  전체 멀티 에이전트 시스템 가동
## ============================================================
## -> State (상태 객체): 
##    * AgentState는 에이전트 간에 정보를 주고받는 공통 메모리. 
##    * 메시지가 쌓이면서 전체 맥락이 유지
##
## -> Conditional Edges (조건부 에지):
##    * supervisor 노드 이후에 어디로 갈지 동적으로 결정하는 부분
##    * 플래닝 기반 멀티툴 에이전트의 심장.
##
## -> Recursive Loop (순환 구조): 
##    * worker_node → supervisor로 돌아옮
##    * 정보가 부족하면 계속해서 도구를 호출하고 보완할 수 있음.
##
## -> Pydantic + Structured Output: 
##    * supervisor가 내린 결정이 정확한 문자열로 반환해야 함.
##    * 그래프가 끊기지 않고 동작함!!
## ============================================================
## ----------------------------
## 모듈 로딩
## ----------------------------
import sys
import os
import json
from typing import TypedDict, Annotated, List, Union
from operator import add

# 프로젝트 루트 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

## 프레임워크 모듈들
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from agents.supervisor_agent import get_supervisor_decision
from agents.worker_agent import worker_executor


## ----------------------------
## [1] 시스템의 상태(State) 정의
## ----------------------------
class AgentState(TypedDict):
    # 모든 메시지 내역을 누적하여 저장 (Annotated[List, add]는 리스트를 합치는 문법)
    messages: Annotated[List[BaseMessage], add]
    # 다음으로 실행할 노드 이름
    next_node: str

## ----------------------------
##  [2] 노드 함수 정의 (Worker 호출용)
##  함수이름 : call_worker
## ----------------------------
def call_worker(state: AgentState):
    """Worker(여행/날씨 전문가)에게 현재 메시지를 전달하고 결과를 받음"""
    last_message = state["messages"][-1]
    # Worker 에이전트(ReAct) 실행
    response = worker_executor.invoke({"messages": [last_message]})
    return {"messages": [response["messages"][-1]]}

## ----------------------------
##  [2] 노드 함수 정의 (Supervisor 호출용)
##  함수이름 : call_supervisor
## ----------------------------
def call_supervisor(state: AgentState):
    """Supervisor가 대화 내역을 보고 다음 노드를 결정"""
    decision = get_supervisor_decision(state["messages"])
    print(f"--- [Supervisor 결정]: {decision.next_node} (사유: {decision.reason}) ---")
    return {"next_node": decision.next_node}


## ----------------------------
##  [3] 그래프(Workflow) 구성
##      - node + state + edge
## ----------------------------
## 그래프 생성 
workflow = StateGraph(AgentState)

# 노드 추가
workflow.add_node("supervisor",  call_supervisor)
workflow.add_node("worker_node", call_worker)

# 시작점 설정
workflow.set_entry_point("supervisor")

# 에지(Edge) 설정: 조건부 분기
workflow.add_conditional_edges(
    "supervisor",
    lambda x: x["next_node"], # Supervisor가 정한 next_node 값에 따라 분기
    {
        "travel_expert": "worker_node",
        "weather_expert": "worker_node",
        "finish": END
    }
)

# Worker가 끝나면 다시 Supervisor에게 돌아가서 다음 단계 확인 (Loop)
workflow.add_edge("worker_node", "supervisor")

# 그래프 컴파일
app = workflow.compile()


## ----------------------------
##  실행 메인 함수
##  함수이름 : main
## ----------------------------
def main():
    user_query = "대한민국의 출산율 현황에 대해 알려줘"
    print(f"질문: {user_query}\n" + "="*50)
    
    config = {"configurable": {"thread_id": "1"}}
    inputs = {"messages": [HumanMessage(content=user_query)]}
    
    # 실행 흐름 출력
    for output in app.stream(inputs, config=config, stream_mode="values"):
        if "messages" in output:
            last_msg = output["messages"][-1]
            if isinstance(last_msg, AIMessage):
                print(f"\n[AI 응답]:\n{last_msg.content}")


## ----------------------------
##  Agent AI Servie 실행
## ----------------------------
if __name__ == "__main__":
    main()
