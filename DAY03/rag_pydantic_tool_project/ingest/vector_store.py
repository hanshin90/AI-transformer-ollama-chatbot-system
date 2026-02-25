## ==========================================================
##                RAG에서 저장소 담당 모듈
##   텍스트를 벡터 변환, 벡터 DB(Chroma)를 로딩하는 역할만 담당
## ==========================================================
## ★★★ ingest와 search가 완전히 같은 임베딩 모델을 사용해야 함
##       다르면 검색 품질 급락
## ==========================================================
## PDF 문서
##  → (ingest/pdf_ingest.py)
##  → vector_store.load_vector_store()
##  → Chroma DB 저장
## ==========================================================
## 사용자 질문
##  → (rag_tool.py)
##  → vector_store.load_vector_store()
##  → similarity_search()
## ==========================================================
## 실무:
##      FAISS (메모리 중심)
##      Weaviate / Pinecone (서버형) 로 교체 가능
## 분리하면
## -> Vector DB 교체가 쉬움
## -> ingest / search 공통 사용
## -> 역할 기반 설계 학습에 좋음
## -> 유지 보수 좋음!!
## ==========================================================
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

## ------------------------------------
## 데이터 벡터 변환 및 DB 저장 
## -> Vector DB를 만들거나 / 불러오는 단일 진입점
## -> ingest 단계와 search 단계에서 공통 사용
## ------------------------------------
def load_vector_store(persist_dir: str):

    # 경량 예제용 임베딩 모델
    embeddings = HuggingFaceEmbeddings(
        # 가볍고 빠름 / 영어/한국어 혼합 문서에 무난 /CPU에서도 사용 가능
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    ## 로컬에서 쉽게 쓸 수 있는 Vector DB
    return Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings
    )
