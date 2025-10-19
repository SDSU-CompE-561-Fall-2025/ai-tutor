# ai-tutor

### Getting Started

_Downloading UV_
`curl -LsSf https://astral.sh/uv/install.sh | sh`

_Getting UV up to standard_
`uv sync`

_Starting the app_ \
`uv run  uvicorn app.main:app --reload --app-dir src --host localhost  --port 3000`

#### .ENV Structure

DATABASE_URL=

CLIENT_ID=

CLIENT_SECRET=

USER_ID=

REDIRECT_URI =

SESSION_SECRET=

FRONTEND_URL=

BACKEND=

PROJECT_ID="gdrive-multiple"
