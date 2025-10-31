# 🧠 AI Tutor Platform — Update Summary

Date: October 30, 2025
Purpose: Summary of the major improvements, files changed, migration steps, and release checklist for the recent backend updates.

## 🔧 Major Fixes and Additions

- Chat messages: Replaced the single `/chat` endpoint with a full chat message model and CRUD endpoints scoped under `/api/v1/chat` and `/api/v1/sessions/{session_id}/messages`.
- Tutor sessions: Added `TutorSession` model with one-to-many relationship to chat messages. Session metadata persisted for search and audit.
- Files & Courses: Added/cleaned file metadata (Drive fields), corrected foreign keys (class/course relations), and clarified constraints.
- Google Drive Integration: Added OAuth flows and MCP endpoints that use stored user tokens to access Drive content.
- Multimedia generation: Added endpoints to produce audio/video summaries using local `movie.py` utilities and Eleven Labs APIs.
- Security & Auth: Password hashing and JWT-based auth added; sensitive routes require bearer auth in OpenAPI.
- Middleware & Errors: Structured HTTP error responses and middleware for CORS, auth, input sanitization, and request logging.

## Files Changed

- Models
    - `src/app/models/chat_message.py`
    - `src/app/models/tutor_session.py`
    - `src/app/models/file.py`
    - `src/app/models/auth_token.py`

- Services / Repository
    - `src/app/services/chat_message.py`
    - `src/app/repository/chat_message.py`
    - `src/app/services/tutor_session.py`
    - `src/app/repository/tutor_session.py`
    - `src/app/services/file.py`
    - `src/app/services/google_drive.py`

- Routes / API
    - `src/app/routes/chat_message.py`
    - `src/app/routes/tutor_session.py`
    - `src/app/routes/file.py`
    - `src/app/api/v1/*`

- Other
    - `movie.py` (multimedia generation helper)
    - `swagger.yaml` (OpenAPI spec)

## Exception & error-handling policy

- Two acceptable patterns:
    1. Services raise FastAPI `HTTPException(status_code=404, detail=...)` for not-found and `HTTPException(status_code=403, ...)` for permission errors — fast and explicit.
    2. Services raise domain exceptions (e.g., `NotFoundError`, `ForbiddenError`) and the application registers global exception handlers mapping them to proper HTTP responses — preferred for larger projects.

## Env vars & secrets
List the environment variables consumers/operators must set:

- `DATABASE_URL` — Postgres connection string
- `SECRET_KEY` — JWT signing key
- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` — for Google Drive OAuth
- `GOOGLE_OAUTH_REDIRECT_URI` — redirect URI used in OAuth flow
- `ELEVEN_LABS_API_KEY` — API key for Eleven Labs (audio generation)
- `SENTRY_DSN` — if Sentry or similar is used

## Reasoning for Changes

In our initial backend design, several critical components and functionalities were missing, which limited the overall capability of the application. As development progressed, it became clear that a more robust and feature-complete backend was essential to support the intended functionality of the AI Tutor platform. Therefore, we expanded the backend architecture to include comprehensive modules for file management, tutoring sessions, chat message handling, and Google Drive integration. These additions transformed the system from a minimal proof of concept into a fully functional platform capable of managing users, content, and interactive AI tutoring experiences.

Additionally, we introduced a short video generation feature that leverages AI to produce concise multimedia summaries of course materials. This enhancement was inspired by the growing popularity and effectiveness of short-form video content in modern learning environments. By integrating video and audio summarization tools using movie.py and Eleven Labs, we aimed to make learning more engaging, accessible, and aligned with current digital content trends.

