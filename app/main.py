# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import Settings
from app.db import init_db
from app.routers.cooking_session import router as cooking_router

settings = Settings()

# Initialize FastAPI application
app = FastAPI(
    title="Chef AI Backend",
    description="Backend untuk ekstraksi bahan, pembuatan resep, dan chat interaktif menggunakan AI.",
    version="1.0.0", 
    docs_url="/docs", # URL for interactive documentation
    redoc_url="/redoc" # URL for alternative documentation
)

# Initialize SQLite database when application starts
@app.on_event("startup")
def on_startup():
    init_db()

# CORS (Cross-Origin Resource Sharing) configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods_list,
    allow_headers=settings.cors_allow_headers_list,
    expose_headers=settings.cors_expose_headers_list,
    max_age=settings.cors_max_age,
)

# Register the integrated router under /api prefix
# All endpoints from cooking_session.py will be available under /api
# Example: /api/session/ , /api/session/{context_id}/chat
app.include_router(cooking_router, prefix="")


@app.get("/", tags=["Root"], summary="Cek Status API")
async def read_root():
    """Endpoint root untuk verifikasi bahwa API berjalan."""
    return {"status": "ok", "message": "Welcome to Chef AI Backend!"}