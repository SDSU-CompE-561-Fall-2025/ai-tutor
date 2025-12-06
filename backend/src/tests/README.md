"""Tests README

# Testing Structure

This directory contains comprehensive unit and integration tests for the AI Tutor backend API.

## Directory Structure

```
tests/
├── conftest.py                # Shared pytest fixtures and configuration
├── unit/                      # Unit tests
│   ├── __init__.py
│   ├── test_user.py          # User model and service tests
│   ├── test_class.py         # Course model and service tests
│   └── test_file.py          # File model and service tests
└── integration/              # Integration tests
    ├── __init__.py
    ├── test_user.py          # User endpoint tests
    ├── test_class.py         # Course endpoint tests
    └── test_file.py          # File endpoint tests
```

## Running Tests

### Prerequisites
```bash
pip install pytest pytest-cov
```

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest tests/unit/test_user.py
pytest tests/integration/test_user.py
```

### Run specific test function
```bash
pytest tests/unit/test_user.py::test_user_registration_validation
```

### Run with coverage
```bash
pytest --cov=app --cov-report=html
```

### Run only unit tests
```bash
pytest tests/unit/
```

### Run only integration tests
```bash
pytest tests/integration/
```

## Test Categories

### Unit Tests

Unit tests focus on individual components in isolation:

**test_user.py**
- User model creation and validation
- Password hashing and verification
- User authentication logic
- Repository operations (CRUD)
- Service layer operations
- Error handling for duplicates and not found

**test_class.py**
- Course model creation
- Course schema validation
- Multiple courses per user
- Course attributes

**test_file.py**
- File model creation
- File schema validation
- Multiple files per user
- Different file types

### Integration Tests

Integration tests test complete workflows through API endpoints:

**test_user.py**
- User login endpoint
- Getting current user profile
- Updating user profile
- Authentication verification
- Error scenarios (invalid credentials, unauthorized access)

**test_class.py**
- Creating courses via API
- Getting course list
- Retrieving specific course
- Updating course details
- Deleting courses
- Complete course workflow

**test_file.py**
- Uploading files
- Getting file list
- Retrieving specific file
- Deleting files
- Complete file workflow

## Fixtures

Common fixtures defined in `conftest.py`:

- `test_db_url`: Temporary SQLite database URL
- `db_engine`: Database engine instance
- `db_session`: Database session for tests
- `client`: FastAPI TestClient
- `test_user_data`: Sample user data
- `registered_user`: Pre-registered user for testing
- `auth_token`: JWT token for authenticated requests
- `authenticated_client`: Client with auth headers
- `test_class_data`: Sample course data
- `test_file_data`: Sample file data

## Best Practices

1. **Isolation**: Each test should be independent
2. **Fixtures**: Reuse fixtures from conftest.py for common setup
3. **Clear Names**: Test function names should describe what they test
4. **Arrange-Act-Assert**: Follow the AAA pattern
5. **Error Cases**: Test both success and failure scenarios
6. **Cleanup**: Fixtures handle automatic cleanup

## Example Test Pattern

```python
def test_example(authenticated_client, db_session):
    # Arrange
    test_data = {"key": "value"}
    
    # Act
    response = authenticated_client.post("/api/endpoint", json=test_data)
    
    # Assert
    assert response.status_code == 200
    assert response.json()["key"] == "value"
```

## CI/CD Integration

To run tests in CI/CD pipeline:

```bash
pytest --verbose --tb=short --junit-xml=test-results.xml
```

## Troubleshooting

### Import errors
Ensure the `src` directory is in the Python path. The conftest.py handles this automatically.

### Database errors
Tests use a temporary SQLite database. Ensure write permissions in the temp directory.

### Fixture scope issues
- `session` scope: Creates one instance for entire test session
- `function` scope: Creates new instance for each test function (default)

## Adding New Tests

When adding new features:
1. Add unit tests in `tests/unit/test_[module].py`
2. Add integration tests in `tests/integration/test_[module].py`
3. Use existing fixtures or create new ones in conftest.py
4. Ensure tests pass locally before committing
5. Aim for >80% code coverage
"""
