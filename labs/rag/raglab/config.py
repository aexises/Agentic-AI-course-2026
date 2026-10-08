from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
DATABASE_URL = 'postgresql://course:course-local-only@127.0.0.1:55432/rag_course'
DIMENSION = 384

def database_url():
    return os.getenv('RAG_DATABASE_URL', DATABASE_URL)

def model_dir():
    return Path(os.getenv('RAG_MODEL_DIR', str(ROOT / 'models'))).resolve()
