import os
from dotenv import load_dotenv

load_dotenv()

# =========================
# GROQ CONFIG
# =========================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "groq")

# =========================
# APP PATHS
# =========================
DATA_DIR = os.getenv("DATA_DIR", "data")
INDEX_DIR = os.getenv("INDEX_DIR", "faiss_index")
DB_PATH = os.getenv("DB_PATH", "database/company.db")
MEMORY_FILE = os.getenv("MEMORY_FILE", "app/memory_store.json")
