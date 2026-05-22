import os
import shutil

from pypdf import PdfReader

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings


from app.core.config import DATA_DIR, INDEX_DIR

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def clear_existing_index():
    if os.path.exists(INDEX_DIR):
        shutil.rmtree(INDEX_DIR)


def extract_text_from_pdf(file_path):

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    return text


def ingest_pdf(file_path, filename):
    text = extract_text_from_pdf(file_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    documents = [
        Document(
            page_content=text,
            metadata={"source": filename}
        )
    ]

    chunks = splitter.split_documents(documents)

    if os.path.exists(INDEX_DIR):
        vector_db = FAISS.load_local(
            INDEX_DIR,
            embedding_model,
            allow_dangerous_deserialization=True
        )

        vector_db.add_documents(chunks)

    else:
        vector_db = FAISS.from_documents(
            chunks,
            embedding_model
        )

    vector_db.save_local(INDEX_DIR)

    return {
        "message": "PDF ingested successfully",
        "filename": filename,
        "chunks": len(chunks)
    }
