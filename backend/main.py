"""
Main FastAPI application for SentimentAlpha Vietnam.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.database import init_db
from backend.routers import signals, sentiment, event_study, settings, watchlist, export, data_management, pipeline

# Create FastAPI app
app = FastAPI(
    title="SentimentAlpha Vietnam API",
    description="API for Vietnamese stock market sentiment analysis and trading signals",
    version="1.0.0"
)

# Configure CORS for frontend - allow all origins for zrok deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for zrok
    allow_credentials=False,  # Must be False when using allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(signals.router)
app.include_router(sentiment.router)
app.include_router(event_study.router)
app.include_router(settings.router)
app.include_router(watchlist.router)
app.include_router(export.router)
app.include_router(data_management.router)
app.include_router(pipeline.router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "SentimentAlpha Vietnam API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment variables
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    
    uvicorn.run(app, host=host, port=port)
