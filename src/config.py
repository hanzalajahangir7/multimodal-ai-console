import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # Allow overriding paths for Serverless/Cloud environments (e.g. use /tmp for Vercel)
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./data/vector_db")
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./data/uploads")

    @staticmethod
    def ensure_dirs():
        # Only attempt to create dirs if they are file-based paths
        if config.VECTOR_DB_PATH.startswith("./") or config.VECTOR_DB_PATH.startswith("/"):
            try:
                os.makedirs(config.VECTOR_DB_PATH, exist_ok=True)
                os.makedirs(config.UPLOAD_DIR, exist_ok=True)
            except OSError as e:
                print(f"Warning: Could not create directories. This might be a read-only filesystem. Error: {e}")

config = Config()
config.ensure_dirs()
