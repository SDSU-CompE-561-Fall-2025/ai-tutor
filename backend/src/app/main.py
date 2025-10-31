from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.routes import api_router
from app.core.database import Base, engine
from app.core.settings import settings

# Create database tables
# If the tables do not exist, create them
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="An API for the Ai Tutor Project.",
    version=settings.app_version,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # only for testing, change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Mount static assets
static_dir = Path(__file__).resolve().parent.parent.parent / "assets"
app.mount("/assets", StaticFiles(directory=static_dir), name="assets")


app.include_router(api_router)
