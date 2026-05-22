from langchain_ollama import ChatOllama
from app.core.config import MODEL_NAME

llm = ChatOllama(
    model=MODEL_NAME,
    temperature=0.1,
    num_predict=200
)
