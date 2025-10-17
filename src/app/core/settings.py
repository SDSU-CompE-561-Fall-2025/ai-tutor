from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    app_name: str = "AI Tutor API"
    app_version: str = "0.1.0"

    secret_key: str = Field(
        default="your_secret_key",
        description="The secret key for JWT",
    )

    algorithm: str = Field(
        default="HS256",
        description="The algorithm used for JWT",
    )

    access_token_expire_minutes: int = Field(
        default=30,
        description="Access token expiration time in minutes",
    )

    database_url: str = Field(
        default="sqlite:///./ai_tutor.db",
        description="Database connection URL",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


settings = Settings()
