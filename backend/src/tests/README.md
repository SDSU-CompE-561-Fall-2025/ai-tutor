# AI Tutor Backend Tests

Comprehensive unit and integration tests for the AI Tutor backend API using Python's `unittest` framework.

## Testing Architecture

The test suite follows a **layered testing approach**:

- **Unit Tests**: Test the **repository layer** (data access) in isolation
- **Integration Tests**: Test the **API route layer** (HTTP endpoints) end-to-end

## Directory Structure

```
tests/
├── base.py                        # Base test class with fixtures and helpers
├── unit/                          # Repository layer tests
│   ├── test_user.py              # UserRepository operations
│   ├── test_course.py            # CourseRepository operations
│   ├── test_file.py              # FileRepository operations
│   ├── test_tutor_session.py     # TutorSessionRepository operations
│   └── test_chat_message.py      # ChatMessageRepository operations
└── integration/                   # API route/endpoint tests
    ├── test_user.py              # User authentication and profile endpoints
    ├── test_course.py            # Course endpoints
    ├── test_file.py              # File upload and retrieval endpoints
    ├── test_tutor_session.py     # Tutor session endpoints
    └── test_chat_message.py      # Chat message endpoints
```
## Running Tests

### Prerequisites

Ensure all dependencies are installed:
```bash
cd backend
uv sync
```

### Run All Tests (Easiest Way)

```bash
# From the backend/src directory (recommended)
cd backend/src
uv run python -m unittest discover -s tests -p "test_*.py" -v
```

Or from the backend directory:
```bash
cd backend
uv run python -m unittest discover -s src/tests -p "test_*.py" -v
```

### Run Tests by Category

**Unit tests only (repository layer):**
```bash
cd backend/src
uv run python -m unittest discover -s tests/unit -p "test_*.py" -v
```

**Integration tests only (API route layer):**
```bash
cd backend/src
uv run python -m unittest discover -s tests/integration -p "test_*.py" -v
```

### Run Specific Test File

```bash
# Unit tests example
uv run python -m unittest src.tests.unit.test_user -v

# Integration tests example
uv run python -m unittest src.tests.integration.test_user -v
```

### Run Specific Test Class or Method

```bash
# Run specific test class
uv run python -m unittest src.tests.unit.test_user.TestUserRepository -v

# Run specific test method
uv run python -m unittest src.tests.unit.test_user.TestUserRepository.test_user_create -v
```

## Test Structure

All tests extend `BaseTestCase` which provides:

- **Database Setup**: Fresh SQLite database per test session
- **Fixtures**: Reusable test data (users, courses, files)
- **Clients**: Unauthenticated and authenticated HTTP clients
- **Helper Methods**: 
  - `create_registered_user()`: Creates a test user via repository
  - `get_auth_token()`: Gets JWT token for authentication
  - `get_authenticated_client()`: Returns client with auth headers
  - `db_session`: Direct database session for setup

### Test Isolation

Each test runs with:
- Fresh database session
- Isolated test data
- No side effects on other tests
- Automatic cleanup after test completion

## Unit Tests (Repository Layer)

Unit tests verify data access layer operations. Each test class has a `setUp()` method that initializes dependencies via repositories before running tests.

### test_user.py

**TestUserRepository**: UserRepository CRUD operations
- `create()`: Create user with hashed password
- `get_by_email()`: Retrieve user by email
- `get_by_id()`: Retrieve user by ID
- Error cases (not found)

**TestUserSchema**: User schema validation
- UserCreate schema validation
- Data type validation

**TestPasswordHandling**: Password utilities
- Password hashing via `get_password_hash()`
- Password verification via `verify_password()`
- Incorrect password rejection

### test_course.py

**TestCourseRepository**: CourseRepository CRUD operations (with UserRepository dependency)
- `create()`: Create course with user
- `get_course_by_name()`: Retrieve by name and user
- `get_course_by_id()`: Retrieve by ID
- `get_all()`: Get all courses for user
- `delete()`: Remove course
- Error cases (not found)

### test_file.py

**TestFileRepository**: FileRepository CRUD operations (with UserRepository dependency)
- `create()`: Create file for user
- `get_file_by_id()`: Retrieve by ID and user
- `get_all()`: Get all files for user
- `delete()`: Remove file
- User isolation verification
- Error cases (not found)

### test_tutor_session.py

**TestTutorSessionRepository**: TutorSessionRepository CRUD operations (with UserRepository and CourseRepository dependencies)
- `create()`: Create session with user and course
- `get_by_id()`: Retrieve by session ID
- `get_by_course()`: Retrieve by course
- `get_by_user()`: Retrieve by user
- `delete()`: Remove session
- Error cases (not found)

### test_chat_message.py

**TestChatMessageRepository**: ChatMessageRepository CRUD operations (with UserRepository, CourseRepository, and TutorSessionRepository dependencies)
- `create()`: Create message with user and session
- `get_message_by_id()`: Retrieve by message ID
- `get_all_messages_by_tutor_session_id()`: Retrieve all for session
- `delete()`: Remove message
- Error cases (not found)

## Integration Tests (API Route Layer)

Integration tests verify complete API workflows through HTTP endpoints. Each test class has a `setUp()` method that initializes dependencies via repositories, then tests HTTP endpoints using `authenticated_client`.

### test_user.py

**TestUserLogin**: User authentication endpoints
- `POST /api/v1/user/login`: Login with valid credentials
- Error: Invalid credentials (401)
- Error: Non-existent email (401)

**TestUserProfile**: User profile endpoints
- `GET /api/v1/user/me`: Get current user (authenticated)
- Error: Get without auth (403)
- `PUT /api/v1/user/me`: Update profile (full and partial)
- Error: Update without auth (403)
- `GET /api/v1/user/token`: Get user OAuth token

### test_course.py

**TestCourseEndpoints**: Course endpoints (requires authenticated user and course)
- `GET /api/v1/courses`: List courses (authenticated)
- Error: List without auth (403)
- `POST /api/v1/courses`: Create course
- Error: Missing fields (422)
- `GET /api/v1/courses/{id}`: Get specific course
- `PUT /api/v1/courses/{id}`: Update course
- `DELETE /api/v1/courses/{id}`: Delete course

### test_file.py

**TestFileEndpoints**: File endpoints (requires authenticated user)
- `GET /api/v1/files`: List files (authenticated)
- Error: List without auth (403)
- `POST /api/v1/files`: Upload file
- Error: Missing fields (422)
- `GET /api/v1/files/{id}`: Get specific file
- `DELETE /api/v1/files/{id}`: Delete file
- Complete workflow: Upload → List → Get → Delete

### test_tutor_session.py

**TestTutorSessionEndpoints**: Tutor session endpoints (requires authenticated user, course, and session)
- `POST /api/v1/tutor-sessions`: Create session
- `GET /api/v1/tutor-sessions`: List sessions
- `GET /api/v1/tutor-sessions/{id}`: Get specific session
- `DELETE /api/v1/tutor-sessions/{id}`: Delete session
- Error: Unauthorized access (403)

### test_chat_message.py

**TestChatMessageEndpoints**: Chat message endpoints (requires authenticated user, course, session, and message)
- `POST /api/v1/chat-messages`: Send message
- `GET /api/v1/tutor-sessions/{id}/chat-messages`: Get session messages
- `GET /api/v1/chat-messages/{id}`: Get specific message
- Complete conversation workflow
- Error: Unauthorized access (403)

## Test Database

Tests use an in-memory SQLite database that:
- Creates fresh database per test session
- Automatically creates all tables from SQLAlchemy models
- Cleans up after all tests complete
- Provides complete isolation between tests

## Architecture Summary

### Data Flow Through Layers

```
API Route (Integration Test) 
    ↓
Route Handler (receives HTTP request)
    ↓
Service Layer (business logic)
    ↓
Repository Layer (Unit Test) ← Data access
    ↓
Database
```

**Unit Tests verify the Repository Layer** - isolated data access operations
**Integration Tests verify the API Route Layer** - complete HTTP workflows

## Debugging Tests

### Verbose Output

```bash
uv run python -m unittest src.tests.unit -v
```

### Run with Debug Output

```bash
uv run python -m unittest src.tests.unit.test_user.TestUserAuthentication.test_user_authentication_success -v
```

### Check Test Discovery

```bash
uv run python -m unittest discover -s src/tests -p "test_*.py" --help
```

## Integration with CI/CD

Tests are designed to run in CI/CD pipelines:

```bash
# Exit with status code reflecting test results
uv run python -m unittest discover -s src/tests -p "test_*.py"

# Generate coverage report
uv run python -m coverage run -m unittest discover -s src/tests
uv run python -m coverage report
```
