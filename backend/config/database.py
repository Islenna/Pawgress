import os
from sqlalchemy import create_engine
from pathlib import Path
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# ✅ Force ENV from system environment, not .env
ENV = os.environ.get("ENV", "development")
env_file = ".env.production" if ENV == "production" else ".env"
env_path = Path(__file__).resolve().parents[1] / env_file
load_dotenv(dotenv_path=env_path, override=True)

print(f"📦 Loaded environment: {ENV} from {env_file}")

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
