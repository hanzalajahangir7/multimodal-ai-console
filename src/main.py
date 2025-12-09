from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router
from src.db.database import engine, Base
from src.config import config
import uvicorn

# Create Tables
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: Database initialization issue: {e}")

app = FastAPI(title="Multi-Modal Intelligence Console", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/files", StaticFiles(directory=config.UPLOAD_DIR), name="files")
app.include_router(router)

@app.get("/")
def read_root():
    return {"status": "online", "message": "Multi-Modal Intelligence Console API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
