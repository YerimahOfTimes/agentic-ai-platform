import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from app.core.config import INDEX_DIR

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def get_vector_db():
    if not os.path.exists(INDEX_DIR):
        return None

    return FAISS.load_local(
        INDEX_DIR,
        embedding_model,
        allow_dangerous_deserialization=True
    )
