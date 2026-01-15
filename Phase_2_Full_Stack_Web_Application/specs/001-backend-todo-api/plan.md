# Implementation Plan: Backend Todo API

**Branch**: `001-backend-todo-api` | **Date**: 2025-12-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-backend-todo-api/spec.md`

## Summary

Build a FastAPI-based REST API for todo management with 6 endpoints (Create, List, Get, Update, Delete, Health) using in-memory storage. The API provides basic CRUD operations without authentication, following clean architecture principles with separation between routes (HTTP layer), services (business logic), and models (data contracts). Implementation uses UV package manager and follows the backend layer architecture defined in the constitution.

**Technical Approach**: Atomic step-by-step implementation starting with FastAPI skeleton, then models, service layer with in-memory storage, routes with proper error handling, and final polish with logging. Each phase is independently testable and delivers incremental value.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI 0.104+, Uvicorn 0.24+, Pydantic 2.5+
**Storage**: In-memory list (acceptable for this phase, data resets on restart)
**Testing**: Manual testing via curl/Postman (pytest integration in future phases)
**Target Platform**: Development server (Linux/Windows/macOS)
**Project Type**: Web backend (dedicated `backend/` folder)
**Performance Goals**: Health check < 100ms, CRUD operations < 500ms, supports 100 sequential operations
**Constraints**: No authentication, no database, no frontend integration, routes must be thin controllers
**Scale/Scope**: Single backend service, 6 REST endpoints, 1 entity (Todo), in-memory storage

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ I. Spec-Driven Workflow
- [x] Specification exists (`specs/001-backend-todo-api/spec.md`)
- [x] Planning phase in progress (this document)
- [ ] Task breakdown (will be `/sp.tasks` output)
- [ ] Implementation (follows tasks)
- [ ] Review (follows implementation)

**Status**: PASS - Following spec-driven workflow correctly

### ✅ II. Layer Separation
- [x] Backend isolated in `backend/` folder
- [x] Routes handle HTTP only (thin controllers)
- [x] Services contain business logic (CRUD operations, validation)
- [x] Models define data contracts (Pydantic)
- [x] NO UI code in backend
- [x] NO SQL in routes (using in-memory storage, no SQL at all)
- [x] NO database access in routes (services handle storage)

**Status**: PASS - Architecture respects layer boundaries

### ✅ III. Backend Architecture
- [x] Structure follows `backend/{main.py, routes/, services/, models/, core/}`
- [x] Routes as thin controllers (delegate to services)
- [x] Services with business logic (validation, CRUD)
- [x] Models for data contracts (TodoCreate, TodoUpdate, TodoResponse)
- [x] No middleware needed (no auth in this phase)

**Status**: PASS - Clean architecture principles followed

### ✅ VIII. Task Definition Standard
- [ ] Tasks will be defined in Phase 2 (`/sp.tasks`)
- [x] Plan provides atomic implementation phases
- [x] Each phase is independently testable

**Status**: PASS - Plan structure supports task definition standard

**Overall Gate Status**: ✅ PASS - All applicable constitution principles satisfied

## Project Structure

### Documentation (this feature)

```text
specs/001-backend-todo-api/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (in progress)
├── research.md          # Phase 0 output (will be created)
├── data-model.md        # Phase 1 output (will be created)
├── quickstart.md        # Phase 1 output (will be created)
├── contracts/           # Phase 1 output (will be created)
│   └── openapi.yaml     # OpenAPI 3.0 specification
├── checklists/          # Quality validation (completed)
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── pyproject.toml       # UV-managed dependencies
├── .venv/               # Python virtual environment
├── main.py              # FastAPI app instance + router registration
├── routes/
│   └── todos.py         # All /api/todos endpoints + /health
├── services/
│   └── todo_service.py  # CRUD logic + in-memory storage
├── models/
│   └── todo.py          # Pydantic models (TodoCreate, TodoUpdate, TodoResponse)
└── core/
    └── config.py        # Settings (port, logging level)
```

**Structure Decision**: Selected "Web application - Backend only" structure since this phase focuses exclusively on backend API. The `backend/` folder is isolated from frontend concerns, following constitution's monorepo structure principle. No `tests/` folder in this phase (manual testing via curl/Postman), but structure accommodates future `backend/tests/` addition.

## Complexity Tracking

> **No violations** - This plan adheres to all constitution principles without exceptions. In-memory storage is explicitly allowed per spec assumptions. No authentication middleware needed per phase scope.

## Phase 0: Research & Technical Decisions

### Objective
Resolve all technical unknowns and document decisions for FastAPI backend implementation with in-memory storage.

### Research Tasks

**Task 0.1: UV Package Manager Setup**
- **Question**: How to initialize and manage Python project with UV?
- **Decision**: Use `uv init .`, `uv venv`, `uv add` workflow
- **Rationale**: UV provides fast, reliable dependency management with lock files. Aligns with user's specified tooling preference.
- **Alternatives**: pip + venv (rejected: slower, no lock file), poetry (rejected: not specified by user)

**Task 0.2: FastAPI Project Structure Best Practices**
- **Question**: How to organize FastAPI routes, services, models for maintainability?
- **Decision**: Adopt APIRouter pattern with separate route files, service layer for business logic, Pydantic models for validation
- **Rationale**: Industry-standard pattern for FastAPI projects. Enables clean separation of HTTP layer from business logic.
- **Alternatives**: Monolithic main.py (rejected: doesn't scale), class-based views (rejected: less idiomatic for FastAPI)

**Task 0.3: In-Memory Storage Strategy**
- **Question**: Best approach for in-memory todo storage?
- **Decision**: Module-level list `todos: List[dict]` in `todo_service.py` with auto-incrementing integer IDs
- **Rationale**: Simple, meets requirements, easy to test, no external dependencies
- **Alternatives**: Redis (rejected: over-engineering), SQLite (rejected: spec says in-memory/file), global dict (rejected: list is more natural for collections)

**Task 0.4: Error Handling Pattern**
- **Question**: How to handle errors consistently in FastAPI?
- **Decision**: Use HTTPException with appropriate status codes, raise from service layer when business rules violated
- **Rationale**: FastAPI's built-in exception handler provides consistent JSON error responses
- **Alternatives**: Custom exception classes (rejected: over-engineering for 6 endpoints), middleware error handler (rejected: not needed for simple API)

**Task 0.5: ID Generation Strategy**
- **Question**: How to generate unique todo IDs?
- **Decision**: Global counter variable, increment on each create, thread-safe enough for development
- **Rationale**: Simple, deterministic, meets spec requirement for auto-incrementing IDs
- **Alternatives**: UUID (rejected: spec requires integer IDs), hash-based (rejected: unnecessary complexity)

**Task 0.6: Timestamp Management**
- **Question**: How to handle created_at and updated_at timestamps?
- **Decision**: Use `datetime.utcnow()` from Python standard library, store as ISO strings, UTC timezone
- **Rationale**: Standard approach, no external dependencies, meets spec requirements
- **Alternatives**: timestamp integers (rejected: less readable), timezone-aware datetimes (rejected: added complexity)

### Outputs
- **research.md**: Consolidate all decisions with rationale, alternatives, and references
- **No unknowns remaining**: All technical questions resolved

## Phase 1: Design & Contracts

### Objective
Design data model, define API contracts, create quickstart guide, and update agent context.

### Task 1.1: Data Model Design

**Output**: `data-model.md`

**Todo Entity**:
- **Fields**:
  - `id` (int): Auto-generated, unique, starts from 1
  - `description` (string): Required, 1-500 characters, non-empty
  - `completed` (boolean): Defaults to false
  - `created_at` (datetime): Auto-populated on creation, UTC, ISO 8601 format
  - `updated_at` (datetime): Auto-updated on modification, UTC, ISO 8601 format

**Validation Rules**:
- description: `min_length=1`, `max_length=500`
- completed: boolean type enforcement
- id: read-only after creation
- timestamps: read-only, system-managed

**State Transitions**:
1. **Create**: `completed=false` → New todo created
2. **Update**: `completed` can toggle true ↔ false, `description` can change
3. **Delete**: Todo removed from storage (no soft delete)

**Relationships**: None (single entity system)

### Task 1.2: API Contracts

**Output**: `contracts/openapi.yaml`

**Endpoints**:

1. **POST /api/todos** - Create Todo
   - Request: `{"description": "string"}` (1-500 chars)
   - Response: 201, TodoResponse
   - Errors: 400 (invalid input), 500 (server error)

2. **GET /api/todos** - List All Todos
   - Response: 200, `List[TodoResponse]`
   - Errors: 500 (server error)

3. **GET /api/todos/{id}** - Get Todo by ID
   - Response: 200, TodoResponse
   - Errors: 404 (not found), 500 (server error)

4. **PATCH /api/todos/{id}** - Update Todo
   - Request: `{"description"?: "string", "completed"?: boolean}` (partial)
   - Response: 200, TodoResponse
   - Errors: 400 (invalid input), 404 (not found), 500 (server error)

5. **DELETE /api/todos/{id}** - Delete Todo
   - Response: 204 No Content
   - Errors: 404 (not found), 500 (server error)

6. **GET /health** - Health Check
   - Response: 200, `{"status": "healthy"}`
   - Errors: 500 (server error)

**Models**:
- **TodoCreate**: `{description: string}`
- **TodoUpdate**: `{description?: string, completed?: boolean}`
- **TodoResponse**: `{id: int, description: string, completed: bool, created_at: datetime, updated_at: datetime}`

Generate OpenAPI 3.0 YAML with full schema definitions, examples, and error responses.

### Task 1.3: Quickstart Guide

**Output**: `quickstart.md`

**Contents**:
1. **Prerequisites**: Python 3.11+, UV installed
2. **Setup Steps**:
   ```bash
   mkdir backend && cd backend
   uv init .
   uv venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   uv add fastapi uvicorn pydantic
   ```
3. **Running Server**: `uvicorn main:app --reload --port 8000`
4. **Testing Endpoints**: curl examples for all 6 endpoints
5. **Expected Responses**: Example JSON for success and error cases
6. **Troubleshooting**: Common issues (port in use, missing dependencies)

### Task 1.4: Agent Context Update

**Action**: Run `.specify/scripts/bash/update-agent-context.sh claude`

**Purpose**: Update Claude-specific context file with:
- Python 3.11+ as project language
- FastAPI, Uvicorn, Pydantic as core dependencies
- Backend-only architecture pattern
- In-memory storage approach

## Implementation Phases (Detailed Breakdown)

### Phase A: FastAPI Skeleton

**Goal**: Create minimal working FastAPI server with health check

**Files to Create**:
1. `backend/pyproject.toml` (UV generates)
2. `backend/main.py`

**main.py Contents**:
```python
from fastapi import FastAPI

app = FastAPI(title="Todo API", version="1.0.0")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

**Acceptance Criteria**:
- [ ] Server starts with `uvicorn main:app --reload`
- [ ] GET /health returns 200 with `{"status": "healthy"}`
- [ ] Response time < 100ms
- [ ] No errors in console

**Testing**: `curl http://localhost:8000/health`

### Phase B: Pydantic Models

**Goal**: Define request/response models for type safety and validation

**File to Create**: `backend/models/todo.py`

**Models**:
```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TodoCreate(BaseModel):
    description: str = Field(..., min_length=1, max_length=500)

class TodoUpdate(BaseModel):
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    completed: Optional[bool] = None

class TodoResponse(BaseModel):
    id: int
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime
```

**Acceptance Criteria**:
- [ ] Models validate correctly (test with valid/invalid data)
- [ ] TodoCreate rejects empty description
- [ ] TodoCreate rejects description > 500 chars
- [ ] TodoUpdate allows partial updates
- [ ] TodoResponse includes all required fields

**Testing**: Python REPL manual validation tests

### Phase C: In-Memory Service Layer

**Goal**: Implement business logic for CRUD operations

**File to Create**: `backend/services/todo_service.py`

**Service Functions**:
```python
from typing import List, Dict, Optional
from datetime import datetime
from fastapi import HTTPException

todos: List[Dict] = []
next_id: int = 1

def create_todo(description: str) -> Dict:
    """Create new todo with auto-generated ID and timestamps"""
    global next_id
    todo = {
        "id": next_id,
        "description": description,
        "completed": False,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    todos.append(todo)
    next_id += 1
    return todo

def list_todos() -> List[Dict]:
    """Return all todos"""
    return todos

def get_todo(todo_id: int) -> Dict:
    """Get todo by ID or raise 404"""
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")

def update_todo(todo_id: int, description: Optional[str], completed: Optional[bool]) -> Dict:
    """Update todo fields and timestamp"""
    todo = get_todo(todo_id)  # Raises 404 if not found
    if description is not None:
        todo["description"] = description
    if completed is not None:
        todo["completed"] = completed
    todo["updated_at"] = datetime.utcnow().isoformat()
    return todo

def delete_todo(todo_id: int) -> None:
    """Delete todo or raise 404"""
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            todos.pop(i)
            return
    raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
```

**Acceptance Criteria**:
- [ ] create() generates unique IDs
- [ ] create() sets completed=False by default
- [ ] list() returns all todos
- [ ] get() returns todo or raises 404
- [ ] update() modifies fields and updates timestamp
- [ ] update() raises 404 for non-existent ID
- [ ] delete() removes todo or raises 404

**Testing**: Python REPL - call functions directly, verify behavior

### Phase D: Route Handlers

**Goal**: Expose service functions via REST endpoints

**File to Create**: `backend/routes/todos.py`

**Router Definition**:
```python
from fastapi import APIRouter, HTTPException, status
from typing import List
from models.todo import TodoCreate, TodoUpdate, TodoResponse
from services import todo_service

router = APIRouter(prefix="/api/todos", tags=["todos"])

@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(data: TodoCreate):
    """Create a new todo item"""
    todo = todo_service.create_todo(data.description)
    return TodoResponse(**todo)

@router.get("", response_model=List[TodoResponse])
async def list_todos():
    """Retrieve all todos"""
    todos = todo_service.list_todos()
    return [TodoResponse(**todo) for todo in todos]

@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int):
    """Get a specific todo by ID"""
    todo = todo_service.get_todo(todo_id)  # Raises HTTPException if not found
    return TodoResponse(**todo)

@router.patch("/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: int, data: TodoUpdate):
    """Update todo description or completion status"""
    todo = todo_service.update_todo(todo_id, data.description, data.completed)
    return TodoResponse(**todo)

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int):
    """Delete a todo item"""
    todo_service.delete_todo(todo_id)  # Raises HTTPException if not found
    return None
```

**Update main.py**:
```python
from fastapi import FastAPI
from routes import todos

app = FastAPI(title="Todo API", version="1.0.0")

# Include todo router
app.include_router(todos.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

**Acceptance Criteria**:
- [ ] POST /api/todos creates todo (201)
- [ ] GET /api/todos lists all todos (200)
- [ ] GET /api/todos/{id} returns todo (200) or 404
- [ ] PATCH /api/todos/{id} updates todo (200) or 404
- [ ] DELETE /api/todos/{id} removes todo (204) or 404
- [ ] All endpoints return proper JSON
- [ ] Error responses include detail message

**Testing**: curl or Postman for all endpoints

### Phase E: Final Polish

**Goal**: Add logging, finalize configuration, end-to-end testing

**File to Create**: `backend/core/config.py`

**Configuration**:
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Todo API"
    port: int = 8000
    log_level: str = "info"

    class Config:
        env_file = ".env"

settings = Settings()
```

**Logging Setup** (in main.py):
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("Todo API starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Todo API shutting down...")
```

**Acceptance Criteria**:
- [ ] Requests logged to console
- [ ] Configuration loaded from env or defaults
- [ ] Full CRUD flow works end-to-end
- [ ] All 8 success criteria from spec validated

**Testing**: Complete workflow test (create → list → get → update → delete)

## Error Handling Strategy

### HTTP Exception Mapping

| Error Condition | HTTP Status | Response Format |
|----------------|-------------|-----------------|
| Empty description | 400 Bad Request | `{"detail": "description must not be empty"}` |
| Description > 500 chars | 400 Bad Request | `{"detail": "description must not exceed 500 characters"}` |
| Invalid JSON | 400 Bad Request | `{"detail": "Invalid JSON format"}` |
| Todo not found | 404 Not Found | `{"detail": "Todo {id} not found"}` |
| Server error | 500 Internal Server Error | `{"detail": "Internal server error"}` |

### Implementation Pattern

- Validation errors: Raised by Pydantic automatically (FastAPI handles)
- Business rule violations: Raise HTTPException from service layer
- Not found: Raise HTTPException 404 from service `get_todo()`
- Unexpected errors: FastAPI default handler (500)

## Running the Backend

**Development Server**:
```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload --port 8000
```

**Access**:
- API Base: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

**Testing Workflow**:
1. Start server
2. Open http://localhost:8000/docs (Swagger UI)
3. Test each endpoint via interactive UI
4. Verify responses match spec acceptance scenarios

## Validation Checklist (End of Plan)

- [x] Constitution principles satisfied
- [x] Technical unknowns resolved (Phase 0 planned)
- [x] Data model designed (Phase 1 planned)
- [x] API contracts defined (Phase 1 planned)
- [x] Implementation phases atomic and testable
- [x] Error handling strategy documented
- [x] No authentication code (per spec)
- [x] Layer separation maintained (routes → services → storage)
- [x] All 6 endpoints planned
- [x] Health check included
- [ ] research.md created (Phase 0 execution pending)
- [ ] data-model.md created (Phase 1 execution pending)
- [ ] contracts/openapi.yaml created (Phase 1 execution pending)
- [ ] quickstart.md created (Phase 1 execution pending)

**Plan Status**: ✅ COMPLETE - Ready for Phase 0 execution

**Next Command**: Continue with Phase 0 (research.md generation) then Phase 1 (data-model, contracts, quickstart)
