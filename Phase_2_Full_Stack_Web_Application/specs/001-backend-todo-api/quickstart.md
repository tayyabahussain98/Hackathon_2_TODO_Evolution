# Quickstart Guide: Backend Todo API

**Feature**: Backend Todo API
**Date**: 2025-12-28
**Purpose**: Get the Todo API running locally in under 5 minutes

## Prerequisites

Before starting, ensure you have:
- **Python 3.11 or higher** installed (`python --version`)
- **UV package manager** installed ([Installation guide](https://github.com/astral-sh/uv))

Verify installations:
```bash
python --version  # Should be 3.11+
uv --version      # Should show uv version
```

## Setup Steps

### Step 1: Create Backend Folder

```bash
mkdir backend
cd backend
```

### Step 2: Initialize Project with UV

```bash
uv init .
```

**Expected Output**: Creates `pyproject.toml` with default configuration

### Step 3: Create Virtual Environment

```bash
uv venv
```

**Expected Output**: Creates `.venv/` directory

### Step 4: Activate Virtual Environment

**Linux/macOS**:
```bash
source .venv/bin/activate
```

**Windows (CMD)**:
```cmd
.venv\Scripts\activate.bat
```

**Windows (PowerShell)**:
```powershell
.venv\Scripts\Activate.ps1
```

**Expected Output**: Command prompt shows `(.venv)` prefix

### Step 5: Install Dependencies

```bash
uv add fastapi uvicorn pydantic
```

**Expected Output**: Packages installed, `pyproject.toml` updated with dependencies

### Step 6: Create Project Structure

The implementation will create these files (see plan.md for details):
```
backend/
├── pyproject.toml      # Already created by UV
├── main.py             # FastAPI app (will be created)
├── routes/
│   └── todos.py        # API endpoints (will be created)
├── services/
│   └── todo_service.py # Business logic (will be created)
├── models/
│   └── todo.py         # Pydantic models (will be created)
└── core/
    └── config.py       # Configuration (will be created)
```

## Running the Server

After implementation is complete:

```bash
cd backend
source .venv/bin/activate  # If not already activated
uvicorn main:app --reload --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Access URLs**:
- API Base: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## Testing the API

### Method 1: Interactive Docs (Recommended for Beginners)

1. Open browser to http://localhost:8000/docs
2. Click on any endpoint to expand
3. Click "Try it out"
4. Fill in request body/parameters
5. Click "Execute"
6. View response below

### Method 2: curl (Command Line)

#### Health Check
```bash
curl http://localhost:8000/health
```

**Expected Response**:
```json
{"status": "healthy"}
```

#### Create Todo
```bash
curl -X POST http://localhost:8000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"description": "Buy groceries"}'
```

**Expected Response** (201 Created):
```json
{
  "id": 1,
  "description": "Buy groceries",
  "completed": false,
  "created_at": "2025-12-28T10:00:00.123456",
  "updated_at": "2025-12-28T10:00:00.123456"
}
```

#### List All Todos
```bash
curl http://localhost:8000/api/todos
```

**Expected Response** (200 OK):
```json
[
  {
    "id": 1,
    "description": "Buy groceries",
    "completed": false,
    "created_at": "2025-12-28T10:00:00.123456",
    "updated_at": "2025-12-28T10:00:00.123456"
  }
]
```

#### Get Single Todo
```bash
curl http://localhost:8000/api/todos/1
```

**Expected Response** (200 OK):
```json
{
  "id": 1,
  "description": "Buy groceries",
  "completed": false,
  "created_at": "2025-12-28T10:00:00.123456",
  "updated_at": "2025-12-28T10:00:00.123456"
}
```

#### Update Todo (Mark Complete)
```bash
curl -X PATCH http://localhost:8000/api/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

**Expected Response** (200 OK):
```json
{
  "id": 1,
  "description": "Buy groceries",
  "completed": true,
  "created_at": "2025-12-28T10:00:00.123456",
  "updated_at": "2025-12-28T10:05:00.789012"
}
```

#### Update Description
```bash
curl -X PATCH http://localhost:8000/api/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"description": "Buy groceries and milk"}'
```

**Expected Response** (200 OK):
```json
{
  "id": 1,
  "description": "Buy groceries and milk",
  "completed": true,
  "created_at": "2025-12-28T10:00:00.123456",
  "updated_at": "2025-12-28T10:10:00.456789"
}
```

#### Delete Todo
```bash
curl -X DELETE http://localhost:8000/api/todos/1
```

**Expected Response**: 204 No Content (no response body)

### Method 3: Postman

1. Import the OpenAPI spec from `contracts/openapi.yaml`
2. Postman auto-generates requests for all endpoints
3. Execute requests in collection
4. View responses and status codes

## Complete Workflow Test

Follow this sequence to test all operations:

```bash
# 1. Health check
curl http://localhost:8000/health

# 2. Create first todo
curl -X POST http://localhost:8000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"description": "Task 1"}'

# 3. Create second todo
curl -X POST http://localhost:8000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"description": "Task 2"}'

# 4. List all todos (should show 2)
curl http://localhost:8000/api/todos

# 5. Get todo by ID
curl http://localhost:8000/api/todos/1

# 6. Update todo (mark complete)
curl -X PATCH http://localhost:8000/api/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# 7. Update description
curl -X PATCH http://localhost:8000/api/todos/2 \
  -H "Content-Type: application/json" \
  -d '{"description": "Updated Task 2"}'

# 8. List todos (verify updates)
curl http://localhost:8000/api/todos

# 9. Delete todo
curl -X DELETE http://localhost:8000/api/todos/1

# 10. Try to get deleted todo (should return 404)
curl http://localhost:8000/api/todos/1

# 11. List remaining todos (should show only ID 2)
curl http://localhost:8000/api/todos
```

## Expected Responses

### Success Responses

| Endpoint | Method | Status | Response Type |
|----------|--------|--------|---------------|
| /health | GET | 200 | `{"status": "healthy"}` |
| /api/todos | POST | 201 | TodoResponse object |
| /api/todos | GET | 200 | Array of TodoResponse |
| /api/todos/{id} | GET | 200 | TodoResponse object |
| /api/todos/{id} | PATCH | 200 | TodoResponse object |
| /api/todos/{id} | DELETE | 204 | No content |

### Error Responses

| Scenario | Status | Response Example |
|----------|--------|------------------|
| Empty description | 400 | `{"detail": "description must not be empty"}` |
| Description too long | 400 | `{"detail": "description must not exceed 500 characters"}` |
| Invalid JSON | 400 | `{"detail": "Invalid JSON format"}` |
| Todo not found | 404 | `{"detail": "Todo 999 not found"}` |
| Server error | 500 | `{"detail": "Internal server error"}` |

## Troubleshooting

### Issue: Port 8000 already in use

**Error**: `[Errno 48] Address already in use`

**Solution**: Use a different port:
```bash
uvicorn main:app --reload --port 8001
```

Or find and kill the process using port 8000:
```bash
# Linux/macOS
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Issue: Module not found errors

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**: Ensure virtual environment is activated and dependencies installed:
```bash
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
uv add fastapi uvicorn pydantic
```

### Issue: Import errors between modules

**Error**: `ImportError: cannot import name 'TodoCreate' from 'models.todo'`

**Solution**: Ensure proper folder structure with `__init__.py` files:
```bash
touch backend/routes/__init__.py
touch backend/services/__init__.py
touch backend/models/__init__.py
touch backend/core/__init__.py
```

### Issue: Validation errors not working

**Error**: Empty descriptions accepted when they shouldn't be

**Solution**: Ensure Pydantic Field validators are configured:
```python
description: str = Field(..., min_length=1, max_length=500)
```

### Issue: CORS errors when testing from browser

**Error**: `Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy`

**Solution**: Add CORS middleware (only if needed for local testing):
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Development Workflow

1. **Start Server**: `uvicorn main:app --reload` (auto-reloads on code changes)
2. **Make Code Changes**: Edit files in backend/
3. **Test Immediately**: Server reloads automatically, test via curl or /docs
4. **Iterate**: Repeat steps 2-3 as needed
5. **Stop Server**: Press `CTRL+C` in terminal

## Next Steps

After completing this quickstart:
1. Review the full specification: `specs/001-backend-todo-api/spec.md`
2. Review the implementation plan: `specs/001-backend-todo-api/plan.md`
3. Run `/sp.tasks` to generate detailed implementation tasks
4. Begin implementation following task order
5. Test each task's acceptance criteria

## Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Pydantic Documentation**: https://docs.pydantic.dev/
- **UV Documentation**: https://github.com/astral-sh/uv
- **OpenAPI Specification**: `specs/001-backend-todo-api/contracts/openapi.yaml`
- **Data Model**: `specs/001-backend-todo-api/data-model.md`

## Quick Reference

**Start Server**:
```bash
cd backend && source .venv/bin/activate && uvicorn main:app --reload
```

**Test Health**:
```bash
curl http://localhost:8000/health
```

**Create Todo**:
```bash
curl -X POST http://localhost:8000/api/todos -H "Content-Type: application/json" -d '{"description": "Test task"}'
```

**List Todos**:
```bash
curl http://localhost:8000/api/todos
```

**Interactive Docs**:
Open http://localhost:8000/docs in browser
