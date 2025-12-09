from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from src.api.routes import router
from src.config import config
import os

# Create FastAPI app
app = FastAPI(title="Multi-Modal Intelligence Console", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
try:
    from src.db.database import engine, Base
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: Database initialization issue: {e}")

# Mount static files only if directory exists
if os.path.exists(config.UPLOAD_DIR):
    try:
        app.mount("/files", StaticFiles(directory=config.UPLOAD_DIR), name="files")
    except Exception as e:
        print(f"Warning: Could not mount static files: {e}")

# Include API routes
app.include_router(router)

# Serve the web UI
@app.get("/", response_class=HTMLResponse)
def read_root():
    try:
        # Try to read the HTML file
        html_path = os.path.join(os.path.dirname(__file__), "..", "public", "index.html")
        if os.path.exists(html_path):
            with open(html_path, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception as e:
        print(f"Could not load HTML: {e}")
    
    # Fallback to API response
    return """
    <html>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>Multi-Modal Intelligence Console API</h1>
            <p>Status: Online ✓</p>
            <p>Visit <a href="/docs">/docs</a> for API documentation</p>
        </body>
    </html>
    """

@app.get("/health")
def health_check():
    return {"status": "healthy", "environment": "vercel" if config.IS_VERCEL else "local"}

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
