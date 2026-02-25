# 사내 규정 RAG 서비스 (Pydantic Tool 기반)

이 프로젝트는 **Pydantic 기반 Tool Schema → Vector DB(Chroma) → RAG 검색 → Agent 실행** 흐름을 실습/시연할 수 있도록 구성했습니다.

## 실행 순서

### 1) 가상환경 생성
```anaconda power shell prompt 관리자 권한으로 실행 
conda env create -f env_agent_ollama_langgraph.yml
```

### 2) 가상환경 활성화
```anaconda power shell prompt 관리자 권한으로 실행
conda activate agent_ollama_langgraph
```

### 3) 패키지 설치
```bash
pip install -r requirements.txt
```

### 4) 모델 설치
```
Ollama 사이트  : https://ollama.com/

OS에 맞는 버전으로 다운로드 후 설치
설치 후 Ollama 실행

명령 프롬프트 실행
cmd
ollama -v       <- 버전 확인
ollama list     <- 설치 모델 리스트 확인

ollama pull qwen2.5:7b   <- Tool Calling 지원 모델 다운로드

```

### 5) PDF 인덱싱(벡터 DB 적재)
```bash
python ingest/pdf_ingest.py
```

### 6) Agent 실행
```bash
python agent/agent_run.py
```

## 참고
- Ollama가 실행 중이어야 하며, tool calling 지원 모델(예: qwen2.5)을 사용하세요.
- `data/hr_policy_2024.pdf`는 예제 규정 PDF입니다.
