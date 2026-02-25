## =========================================================
## [2] 실제 PDF 사내 규정 예제
## - PDF 로딩 + 청크 분할
## - 실제 PDF → Vector DB
## - RAG Tool이 실제 규정 문서 기반으로 답변
## =========================================================
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from vector_store import load_vector_store

vector_db = load_vector_store()

loader = PyPDFLoader("hr_policy_2024.pdf")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)

# 메타데이터 추가
for c in chunks:
    c.metadata.update({
        "doc_type": "HR_POLICY",
        "year": 2024
    })

vector_db.add_documents(chunks)
vector_db.persist()