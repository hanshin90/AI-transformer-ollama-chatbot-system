## ============================================================
##                   도구 실행 자동화 ToolNode 생성
## ============================================================
## -> LLM은 "계산기를 써야겠다"라고 판단(Tool Calling)만 함
## -> 실제로 계산기 버튼을 누르지는 못함!!!
##
## ※ ToolNode
##    LLM이 선택한 도구(이름과 인자)를 받아서 파이썬 코드로 실제 실행
##    그 결과값을 다시 메시지 형태로 돌려주는 자동 실행기 역할
## 
## ※ 워크플로우 그래프에서의 위치
## -> Supervisor/Worker: 메시지를 던짐.
## -> ToolNode (이 파일): 그 메시지를 낚아채서 실행할 함수를 실제로 호출.
## -> ToolNode: 실행 결과를 메시지에 담아 다시 워크플로우로 반환.
## ============================================================
## -----------------------------------
## 모듈 로딩
## -----------------------------------
from langgraph.prebuilt import ToolNode
from tools.travel_tool import travel_tool
from tools.weather_tool import weather_tool

tools = [travel_tool, weather_tool]
tool_node = ToolNode(tools) # 에이전트가 호출할 도구들의 집합
