## ==================================================================
##                  Agent AI Service 구동 파일
## ==================================================================
## ---------------------------------------
## 모듈 로딩
## ---------------------------------------
from __future__ import annotations

## 기본 모듈 : 다른 py파일 불러오기
import sys
import os

# 프로젝트 루트 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# langChain 의 ollama 관련
from langchain_ollama import ChatOllama

#사용자 개발용 Tool, Agent 모듈
from tools.calculator_tool import calculator_tool
from tools.worker_dispatch_tool import build_worker_dispatch_tool
from agents.worker_agent import create_worker_agent
from agents.supervisor_agent import create_supervisor_agent

## LLM Model 설정
LLM_MODEL = "qwen2.5:7b"

## ---------------------------------------
## Agent AI Service 실행 함수 
## ---------------------------------------
def main():
    # Tool calling 지원 모델 사용 권장
    llm = ChatOllama(model=LLM_MODEL)

    # 1) Worker: 실제 실행 담당 (calculator tool 사용 가능)
    worker = create_worker_agent(llm, tools=[calculator_tool])

    # 2) Supervisor: 판단/조정 담당 (worker를 tool로 호출 가능)
    worker_dispatch_tool = build_worker_dispatch_tool(worker)
    supervisor = create_supervisor_agent(llm, tools=[worker_dispatch_tool])

    #사용자 정의
    while True:
        print("=" * 80)
        query = input("[질문] 입력하세요. (종료: X)>>")
        if query in ['X', 'x']:
            print("고객 요청으로 종료합니다.")
            break
        result = supervisor.invoke({"messages": [("user", query)]})
        print("[답변] ", result["messages"][-1].content)
'''
    # 테스트 입력
    queries = [
        "안녕하세요. 오늘 수업 목표를 한 문장으로 설명해줘.",
        "12 * (3 + 4) 계산해줘.",
        "연봉 4500만원에서 월급(세전) 대략 얼마인지 간단히 계산해줘. 계산 과정은 짧게."
    ]

    for q in queries:
        print("=" * 80)
        print("USER:", q)
        result = supervisor.invoke({"messages": [("user", q)]})
        print("ASSISTANT:", result["messages"][-1].content)'''

        
## ---------------------------------------
## Agent AI Service 실행 
## ---------------------------------------
if __name__ == "__main__":
    main()
