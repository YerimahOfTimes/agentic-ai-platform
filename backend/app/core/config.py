import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "phi3")

DATA_DIR = os.getenv("DATA_DIR", "data")
INDEX_DIR = os.getenv("INDEX_DIR", "faiss_index")
DB_PATH = os.getenv("DB_PATH", "database/company.db")
MEMORY_FILE = os.getenv("MEMORY_FILE", "app/memory_store.json")
