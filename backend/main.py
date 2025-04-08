import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from config.database import Base
from models.User import User
from models.Skill import Skill

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
from routes.users import UserRouter
from routes.skills import SkillRouter
app.include_router(UserRouter, prefix="/api", tags=["Users"])
app.include_router(SkillRouter, prefix="/api", tags=["Skills"])
