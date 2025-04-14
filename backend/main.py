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
from models.Category import Category
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


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

# Static files

STATIC_DIR = Path(__file__).resolve().parent / "static"
# Create static and ce_docs directories if they don't exist
STATIC_DIR.mkdir(exist_ok=True)
(STATIC_DIR / "ce_docs").mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
print(f"📂 Serving static files from: {STATIC_DIR}")



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print("Validation Error:", exc.errors())
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )
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
from routes.categories import CategoryRouter
from routes.proficiencies import ProficiencyRouter
from routes.CEs import CERouter
from routes.shoutouts import ShoutoutRouter
from routes.auth import AuthRouter

app.include_router(UserRouter, prefix="/api", tags=["Users"])
app.include_router(SkillRouter, prefix="/api", tags=["Skills"])
app.include_router(CategoryRouter, prefix="/api", tags=["Categories"])
app.include_router(ProficiencyRouter, prefix="/api", tags=["Proficiencies"])
app.include_router(CERouter, prefix="/api", tags=["CEs"])
app.include_router(ShoutoutRouter, prefix="/api", tags=["Shoutouts"])
app.include_router(AuthRouter, prefix="/api", tags=["Auth"])
