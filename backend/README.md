# ai-tutor

### Getting Started

_Downloading UV_
`curl -LsSf https://astral.sh/uv/install.sh | sh`

_Getting UV up to standard (downloading all dependencies)_
`uv sync`

_Starting the MCP Server_
`PYTHONPATH=src uv run python -m app.mcp.server.main`

_Starting the app_
`uv run  uvicorn app.main:app --reload --app-dir src --host localhost  --port 3000`

_Accessing Swagger Docs_
`http://localhost:3000/docs`

#### .ENV Structure

DATABASE_URL=

CLIENT_ID=

CLIENT_SECRET=

REDIRECT_URI =

SESSION_SECRET=

FRONTEND_URL=

BACKEND=

MCP_SERVER="http://127.0.0.1:8000/mcp"

PROJECT_ID="gdrive-multiple"

FERNET_KEY= `openssl rand -base64 32 | tr '+/' '-*' | tr -d '='` run this in terminal

OPENAI_KEY=

ELEVEN_KEY=

GEMINI_KEY=
