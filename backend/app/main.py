import os
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from app.graph.workflow import workflow
from app.rag.ingest import ingest_pdf
from app.memory import add_to_memory, clear_memory
import shutil
from app.core.config import MODEL_NAME

app = FastAPI()

graph = workflow  # ✅ FIXED


class QuestionRequest(BaseModel):
    question: str
    session_id: str = "default"


@app.get("/")
def home():
    return {"message": "Agentic AI running"}


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    os.makedirs("data", exist_ok=True)

    file_path = f"data/{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    result = ingest_pdf(
        file_path=file_path,
        filename=file.filename
    )

    return result


@app.post("/ask")
def ask(req: QuestionRequest):
    print("🔥 HIT /ask ENDPOINT")

    result = graph.invoke({
        "question": req.question,
        "session_id": req.session_id
    })

    answer = result.get("final_answer")

    add_to_memory(req.session_id, "user", req.question)
    add_to_memory(req.session_id, "assistant", answer)

    return {
        "response": answer,
        "sources": result.get("sources", []),
        "trace": result.get("trace", [])
    }


@app.post("/clear-memory/{session_id}")
def reset_memory(session_id: str):
    clear_memory(session_id)
    return {"message": f"Memory cleared for {session_id}"}


@app.delete("/clear-documents")
def clear_documents():
    if os.path.exists("faiss_index"):
        shutil.rmtree("faiss_index")

    return {"message": "All uploaded document indexes cleared"}


@app.get("/status")
def status():
    return {
        "status": "running",
        "model": MODEL_NAME,
        "features": {
            "calculator": True,
            "python_tool": True,
            "web_search": True,
            "sql_tool": True,
            "pdf_rag": True,
            "session_memory": True,
            "persistent_memory": True,
            "agent_trace": True
        }
    }
