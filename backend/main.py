import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from backend.config.database import Base
from backend.models.User import User
from backend.models.Skill import Skill
from backend.models.Category import Category

# Load environment variables
load_dotenv()

# Get environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
ORIGINS = os.getenv("ALLOWED_ORIGINS")
DB_NAME = DATABASE_URL.split("/")[-1]
BASE_URL = DATABASE_URL.rsplit("/", 1)[0]

# Create a temporary engine WITHOUT the DB name to create it
def create_database_if_not_exists():
    print("🔍 Checking for database...")
    temp_engine = create_engine(BASE_URL)
    try:
        with temp_engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};"))
            print(f"✅ Database '{DB_NAME}' is ready.")
    except OperationalError as e:
        print("❌ Could not create database:", e)

create_database_if_not_exists()

#Connect to the actual DB
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

#Initialize FastAPI
print("🚀 App is starting!")
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from Pawgress!"}

#CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS.split(",") if ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#Routes
from backend.routes.users import UserRouter
from backend.routes.skills import SkillRouter
from backend.routes.categories import CategoryRouter
from backend.routes.proficiencies import ProficiencyRouter
from backend.routes.CEs import CERouter
from backend.routes.auth import AuthRouter

app.include_router(UserRouter, prefix="/api", tags=["Users"])
app.include_router(SkillRouter, prefix="/api", tags=["Skills"])
app.include_router(CategoryRouter, prefix="/api", tags=["Categories"])
app.include_router(ProficiencyRouter, prefix="/api", tags=["Proficiencies"])
app.include_router(CERouter, prefix="/api", tags=["CEs"])
app.include_router(AuthRouter, prefix="/api", tags=["Auth"])
