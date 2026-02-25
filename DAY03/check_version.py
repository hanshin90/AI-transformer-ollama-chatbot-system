import langgraph
import langchain
from importlib.metadata import version

# 버전을 변수에 저장
langgraph_v = version("langgraph")
langchain_v = version("langchain")

# 화면에 출력
print(f"LangGraph 버전: {langgraph_v}")
print(f"LangChain 버전: {langchain_v}")