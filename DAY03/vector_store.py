## =========================================================
## Vector DB (Chroma) + Embedding
## =========================================================

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

def load_vector_store(persist_dir="./chroma_db"):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings
    )