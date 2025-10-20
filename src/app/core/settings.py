from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

# Load .env file early
load_dotenv()


class Settings(BaseSettings):
    # --- App Info ---
    app_name: str = "AI Tutor API"
    app_version: str = "0.1.0"

    # --- JWT Auth ---
    secret_key: str = Field(default="your_secret_key", description="Secret key for JWT")
    algorithm: str = Field(default="HS256", description="Algorithm used for JWT")
    access_token_expire_minutes: int = Field(
        default=30,
        description="Token expiration (minutes)",
    )

    # --- Database ---
    database_url: str = Field(
        default="sqlite:///./ai_tutor.db",
        description="Database connection URL",
    )

    # --- Google OAuth2 ---
    client_id: str = Field(
        default="your_client_id.apps.googleusercontent.com",
        description="Google OAuth2 client ID",
    )
    client_secret: str = Field(
        default="your_client_secret",
        description="Google OAuth2 client secret",
    )
    redirect_uri: str = Field(
        default="http://localhost:3000/api/v1/user/auth/google/callback",
        description="Redirect URI for OAuth2",
    )
    token_uri: str = Field(
        default="https://oauth2.googleapis.com/token",
        description="Google token exchange endpoint",
    )

    # --- Session & URLs ---
    session_secret: str = Field(
        default="your-super-secret-session-key-change-in-production",
        description="Session secret key for cookies/sessions",
    )
    frontend_url: str = Field(
        default="http://localhost:5173",
        description="Frontend URL",
    )
    backend_url: str = Field(
        default="http://localhost:3000",
        description="Backend API URL",
    )
    project_id: str = Field(
        default="gdrive-multiple",
        description="Google Cloud project ID",
    )
    mcp_server: str = Field(
        default="http://127.0.0.1:8000/mcp",
        description="FastMCP server URL",
    )
    fernet_key: str = Field(
        default="feret_secret_key",
        description="Secret key used to encrypt and decrypt google oauth2 tokens",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"
        fernet_key: str


settings = Settings()
