import os

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from app.core.config import INDEX_DIR


_embedding_model = None


def get_embedding_model():
    global _embedding_model

    if _embedding_model is None:
        _embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    return _embedding_model


def get_vector_db():
    if not os.path.exists(INDEX_DIR):
        return None

    embedding_model = get_embedding_model()

    return FAISS.load_local(
        INDEX_DIR,
        embedding_model,
        allow_dangerous_deserialization=True
    )
