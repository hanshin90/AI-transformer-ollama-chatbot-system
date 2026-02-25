import os
import sys

# 프로젝트 루트 경로를 PYTHONPATH에 추가 (직접 실행 안정화)
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ingest.vector_store import load_vector_store

def main():
    persist_dir = os.path.join(ROOT, "chroma_db")
    vector_db = load_vector_store(persist_dir=persist_dir)

    pdf_path = os.path.join(ROOT, "data", "hr_policy_2024.pdf")
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)

    # 메타데이터(필터용) 부여
    for c in chunks:
        c.metadata.update({
            "doc_type": "HR_POLICY",
            "year": 2024
        })

    vector_db.add_documents(chunks)
    vector_db.persist()

    print("✅ PDF 인덱싱 완료")
    print(f"- Persist dir: {persist_dir}")
    print(f"- Chunks: {len(chunks)}")

if __name__ == "__main__":
    main()
