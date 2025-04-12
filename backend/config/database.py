import os
from sqlalchemy import create_engine
from pathlib import Path
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 🔥 Load the .env file cleanly from project root
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

# ✅ Now read DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print(f"🔍 Tried loading env from: {env_path}")
    raise RuntimeError("❌ DATABASE_URL not found. Is your .env in the project root?")

print("🧪 DATABASE_URL =", DATABASE_URL)

# ✅ Set up SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
