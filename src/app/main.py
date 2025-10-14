from fastapi import FastAPI

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

app.include_router(api_router)
