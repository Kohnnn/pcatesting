"""
Database connection and session management for FastAPI.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import sys
import os

# Add src to path to import models
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.database import Base

# Database configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", "sentimentalpha.db")
DATABASE_URL = f"sqlite:///./{DATABASE_PATH}"

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.
    
    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
