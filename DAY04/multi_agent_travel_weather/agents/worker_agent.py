## ============================================================
##                      Worker Agent 생성   
## ============================================================
## -> 특정 작업(여행지 추천, 날씨 조회)에 특화된 역할을 수행
## -> 전달받은 도구를 어떻게 정확히 쓸지 결정 
## ============================================================
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from tools.travel_tool import travel_tool
from tools.weather_tool import weather_tool


## ---------------------------------------
## [1] Worker Agent 생성위한 준비 
## ---------------------------------------
## 분석 + 계획하는 LLM 모델
LLM_MODEL = "qwen2.5:7b"

## 실행을 담당하는 Worker용 LLM 설정
llm = ChatOllama(model=LLM_MODEL, temperature=0)

## 도구들을 모아서 Worker 에이전트 생성
tools = [travel_tool, weather_tool]

## ---------------------------------------
## [2] Worker Agent 생성 
## ---------------------------------------
## -> 도구를 실제로 실행하고 결과를 반환하는 역할만 수행
worker_executor = create_agent(llm, tools)
