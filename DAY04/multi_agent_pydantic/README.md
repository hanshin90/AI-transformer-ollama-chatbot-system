# Multi-Agent (Pydantic + StructuredTool) Example

이 프로젝트는 멀티 Agent 연동을 최신 흐름에 가깝게 실습할 수 있도록,
Tool을 Pydantic Schema + StructuredTool로 구성한 예제입니다.

## 구성
- agents/supervisor_agent.py : Supervisor (의사결정/조정)
- agents/worker_agent.py     : Worker (실행)
- tools/*.py                 : StructuredTool 정의 (Pydantic 입력 스키마 포함)
- schemas/*.py               : Pydantic 입력 스키마
- agent/run.py               : 실행 엔트리 포인트

## 실행 전 준비
1) Ollama 설치 및 실행
2) 모델 설치 (예: qwen2.5)
   - ollama pull qwen2.5:7b

## 설치
```bash
pip install -r requirements.txt
```

## 실행
```bash
python -m agent.run
```

## 참고
- 이 예제는 "LLM이 도구를 호출"하는 형태입니다.
- Tool Calling을 지원하는 Ollama 모델을 사용하세요.
