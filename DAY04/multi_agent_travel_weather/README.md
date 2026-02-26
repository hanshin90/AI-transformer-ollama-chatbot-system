# Multi-Agent (Pydantic + StructuredTool) Example

이 프로젝트는 플래닝 기반 멀티 에이전트의 핵심 원리인 의사결정(Planning)과 도구 실행(Execution)을 실습하기 위한 예제입니다. 
최신 에이전트 설계 패턴인 Pydantic 스키마와 StructuredTool을 활용하여 데이터의 안정성을 높였습니다.

## 핵심 특징
- Pydantic 기반 입력 검증     : LLM이 도구에 잘못된 인자를 넘기지 않도록 강제
- StructuredTool 활용        : 도구의 이름, 설명, 입력 구조를 명확히 정의하여 LLM의 도구 호출 성공률을 높임.
- 모듈화된 구조               : 스키마, 도구, 에이전트 로직을 분리하여 확장성을 확보.

## 구성
multi_agent_project/
├─ agent/
│  └─ agent_run.py          # 실행 엔트리 포인트 (Main)
├─ agents/
│  ├─ supervisor_agent.py   # Supervisor (전체 계획 수립 및 Worker 배분)
│  └─ worker_agent.py       # Worker (실제 도구를 사용하는 실행 에이전트)
├─ schemas/
│  ├─ travel_schema.py       # 여행지 추천 입력 스키마 (Pydantic)
│  └─ weather_schema.py      # 날씨 조회 입력 스키마 (Pydantic)
├─ tools/
│  ├─ travel_tool.py        # 여행지 추천 StructuredTool 정의
│  └─ weather_tool.py        # 날씨 조회 StructuredTool 정의
├─ requirements.txt         # 필수 라이브러리 목록
└─ README.md                # 프로젝트 가이드

- agents/supervisor_agent.py : Supervisor (의사결정/조정)
- agents/worker_agent.py     : Worker (실행)
- tools/*.py                 : StructuredTool 정의 (Pydantic 입력 스키마 포함)
- schemas/*.py               : Pydantic 입력 스키마
- agent/run.py               : 실행 엔트리 포인트

## 실행 전 준비
1) Ollama 설치 및 실행
2) 모델 설치 (예: qwen2.5)
   - ollama pull qwen2.5:7b

## 실행 전 준비
1) 가상환경 생성 및 라이브러리 설치


## 설치
```bash
pip install -r requirements.txt
```

## 실행
```bash
python -m agent.run
```

## 참고
- 이 예제는 LLM이 도구를 호출하는 형태
- Tool Calling을 지원하는 Ollama 모델을 사용
