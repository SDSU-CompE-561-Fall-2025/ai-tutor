import os

import requests
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid",
]


def generateOAuth2Client() -> Flow:  # noqa: N802
    """
    Generate oAuth2Client using Flow
    """
    return Flow.from_client_config(
        {
            "web": {
                "client_id": os.getenv("CLIENT_ID"),
                "project_id": os.getenv("PROJECT_ID"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": os.getenv("CLIENT_SECRET"),
                "redirect_uris": [os.getenv("REDIRECT_URI")],
                "javascript_origins": [os.getenv("BACKEND_SERVER")],
            },
        },
        SCOPES,
    )


def get_auth_url() -> tuple[str, str]:
    """
    Get and Return google AUTH URL
    """
    flow = generateOAuth2Client()
    flow.redirect_uri = os.getenv("REDIRECT_URI")
    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    return auth_url, state


def handle_oauth_callback(auth_code: str) -> dict:
    """
    Exchange the 'code' parameter from Google's redirect for access/refresh tokens.
    """
    flow = generateOAuth2Client()
    flow.redirect_uri = os.getenv("REDIRECT_URI")

    # Exchange the code for tokens
    flow.fetch_token(code=auth_code)

    credentials = flow.credentials
    return {
        "access_token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": getattr(
            credentials,
            "token_uri",
            "https://oauth2.googleapis.com/token",
        ),
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
        "expiry": credentials.expiry.isoformat() if credentials.expiry else None,
    }


def refresh_credentials(refresh_token: str) -> dict:
    """
    Refresh expired access tokens using a stored refresh token.
    """
    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri=os.getenv("TOKEN_URI"),
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        scopes=SCOPES,
    )

    # Refresh the access token
    creds.refresh(Request())
    return {
        "access_token": creds.token,
        "refresh_token": creds.refresh_token,
        "expiry": creds.expiry.isoformat() if creds.expiry else None,
    }


def get_google_email(access_token: str) -> str:
    try:
        r = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo?alt=json",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=5,
        )
    except requests.Timeout:
        return "Google API request timed out"
    r.raise_for_status()
    data = r.json()
    return data.get("email")
