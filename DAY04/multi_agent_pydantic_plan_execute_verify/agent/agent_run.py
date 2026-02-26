import sys
import os

#전체 agent system 작업흐름도/설계도 생성
from graph.graph_builder import build_graph

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#agent system 실행 함수
def main():
    graph = build_graph()
    result = graph.invoke({
        "messages": [("user", "12 * (3 + 4) 계산해줘")]
    })
    print(result)

if __name__ == "__main__":
    main()
