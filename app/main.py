# app/main.py

import os
import sys
import traceback
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import Settings
from app.db import init_db
from app.routers.cooking_session import router as cooking_router

try:
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
        try:
            init_db()
            print("Database initialized successfully")
        except Exception as e:
            print(f"Error initializing database: {e}")
            traceback.print_exc()
    
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
        # Basic response without exposing environment variables in production
        response = {
            "status": "ok", 
            "message": "Welcome to Chef AI Backend!"
        }
        
        # Add environment variables info only in debug mode
        if settings.debug_mode:
            response["env_vars"] = {
                "database_url": os.environ.get("DATABASE_URL", "Not set"),
                "cors_origins": os.environ.get("CORS_ORIGINS", "Not set"),
                "openrouter_model": os.environ.get("OPENROUTER_MODEL", "Not set"),
                # Don't expose API key
                "openrouter_api_key": "***" if os.environ.get("OPENROUTER_API_KEY") else "Not set",
                # Print Python version for debugging
                "python_version": sys.version
            }
            
        return response
    
    # Debug endpoint to help diagnose issues - only available when debug_mode is True
    if settings.debug_mode:
        @app.get("/debug", tags=["Debug"], summary="Debug Info")
        async def debug_info():
            """Debugging endpoint to check environment configuration."""
            try:
                return {
                    "status": "ok",
                    "cors_config": {
                        "origins": settings.cors_origins_list,
                        "methods": settings.cors_allow_methods_list,
                        "headers": settings.cors_allow_headers_list,
                        "credentials": settings.cors_allow_credentials,
                    },
                    "env_vars": {
                        "database_url": os.environ.get("DATABASE_URL", "Not set"),
                        "python_version": sys.version,
                    }
                }
            except Exception as e:
                return {"status": "error", "message": str(e), "traceback": traceback.format_exc()}

except Exception as e:
    # This helps diagnose startup errors in Heroku
    print(f"ERROR DURING APP INITIALIZATION: {e}")
    traceback.print_exc()
    
    # Create a minimal app that explains the error
    app = FastAPI(title="Chef AI Backend - ERROR MODE")
    
    @app.get("/")
    async def error_root():
        return {
            "status": "error",
            "message": f"Application failed to initialize: {str(e)}",
            "traceback": traceback.format_exc(),
            "python_version": sys.version,
            "environment": {k: "***" if k.lower().find("key") >= 0 else v for k, v in os.environ.items()}
        }