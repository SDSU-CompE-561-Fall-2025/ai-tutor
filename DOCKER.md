# AI Tutor - Docker Setup

This directory contains Docker configuration files to run the AI Tutor application using Docker and Docker Compose.

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)

## Quick Start

1. **Set up environment variables**
   
   Make sure your backend `.env` file has the necessary credentials:
   ```bash
   cd backend
   # Edit .env file with your API keys and secrets
   ```

2. **Build and run the containers**
   
   From the project root directory:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:3000
   - API Documentation: http://localhost:3000/docs

## Individual Services

### Backend

Build and run backend only:
```bash
cd backend
docker build -t ai-tutor-backend .
docker run -p 3000:3000 ai-tutor-backend
```

### Frontend

Build and run frontend only:
```bash
cd frontend
docker build -t ai-tutor-frontend .
docker run -p 5173:5173 ai-tutor-frontend
```

## Docker Compose Commands

**Start services in detached mode:**
```bash
docker-compose up -d
```

**Stop services:**
```bash
docker-compose down
```

**View logs:**
```bash
docker-compose logs -f
```

**Rebuild containers:**
```bash
docker-compose up --build
```

**Remove all containers and volumes:**
```bash
docker-compose down -v
```

## Environment Variables

Key environment variables for the services:

### Backend
- `DATABASE_URL`: Database connection string
- `CLIENT_ID`: Google OAuth client ID
- `CLIENT_SECRET`: Google OAuth client secret
- `FERNET_KEY`: Encryption key
- `SESSION_SECRET`: Session secret key

### Frontend
- `NEXT_PUBLIC_API_URL`: Backend API URL

You can override these in the `docker-compose.yml` file or create a `.env` file in the root directory.

## File Structure

```
.
├── backend/
│   ├── Dockerfile          # Backend container definition
│   └── .dockerignore       # Files to exclude from backend image
├── frontend/
│   ├── Dockerfile          # Frontend container definition
│   └── .dockerignore       # Files to exclude from frontend image
├── docker-compose.yml      # Multi-container orchestration
└── .dockerignore           # Root-level exclusions
```

## Notes

- The SQLite database is mounted as a volume to persist data
- Backend runs on port 3000 with hot-reload enabled
- Frontend runs in production mode on port 5173
- Both services are connected via a Docker network for internal communication
- Assets directory is mounted for backend file storage

## Troubleshooting

**Port already in use:**
```bash
# Change the port mapping in docker-compose.yml
ports:
  - "8000:3000"  # Map to different host port
```

**Permission issues:**
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
```

**Clean rebuild:**
```bash
docker-compose down
docker system prune -a
docker-compose up --build
```
