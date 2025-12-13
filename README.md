# 🎓 AI Tutor Assistant

AI Tutor is a comprehensive learning platform that helps students study smarter. After signing up with Google authentication, students can create courses (classes), attach relevant documents from Google Drive, and interact with an AI model to understand, summarize, and quiz themselves on the material. Beyond basic Q&A, the platform provides AI-powered tutoring, educational video generation, and learning insights to help students better retain knowledge and prepare for exams.

## 🛠 Tech Stack

**Backend:** FastAPI • Python 3.11 • SQLAlchemy • Google Gemini • OpenAI • ElevenLabs

**Frontend:** Next.js 14 • TypeScript • Tailwind CSS • React Context API

**Infrastructure:** Docker • GitHub Actions

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- uv (Python package manager)
- Docker (optional)

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ai-tutor.git
   cd ai-tutor
   ```

2. **Set up environment variables:**
   
   Create a `.env` file in the `backend/` directory (see [Environment Variables](#environment-variables) section)

3. **Start the backend:**
   ```bash
   cd backend
   uv sync
   uv run uvicorn app.main:app --reload --app-dir src --host localhost --port 3000
   ```

4. **Start the MCP server** (in a new terminal):
   ```bash
   cd backend
   PYTHONPATH=src uv run python -m app.mcp.server.main
   ```

5. **Start the frontend** (in a new terminal):
   ```bash
   cd frontend
   npm install
   npm run dev -- -p 5173
   ```

6. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:3000
   - API Docs: http://localhost:3000/docs

### Using Docker

```bash
# Build and start all services
docker-compose build

# Run in detached mode
docker-compose up -d

# Stop services
docker-compose down
```

## 🔑 Environment Variables

Create a `.env` file in `backend/` with:

```env
# Database
DATABASE_URL=sqlite:///./ai_tutor.db

# Google OAuth
CLIENT_ID=your_google_client_id
CLIENT_SECRET=your_google_client_secret
REDIRECT_URI=redirect_url

# API Keys
GEMINI_KEY=your_gemini_api_key
OPENAI_KEY=your_openai_api_key
ELEVEN_KEY=your_elevenlabs_api_key

# Encryption
FERNET_KEY=your_fernet_encryption_key

# URLs
FRONTEND_URL=frontend_url
BACKEND_URL=backend_url
MCP_SERVER=mcp_server_url
```

## 📁 Project Structure

```
ai-tutor/
├── backend/              # FastAPI backend
│   ├── src/app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Configuration & auth
│   │   ├── models/      # Database models
│   │   ├── services/    # Business logic
│   │   └── schemas/     # Pydantic schemas
│   └── Dockerfile
├── frontend/            # Next.js frontend
│   ├── app/            # App router pages
│   ├── components/     # React components
│   ├── contexts/       # Context providers
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```