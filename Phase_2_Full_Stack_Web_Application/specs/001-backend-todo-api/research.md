# Technical Research: Backend Todo API

**Feature**: Backend Todo API
**Date**: 2025-12-28
**Purpose**: Document all technical decisions, alternatives considered, and rationale for FastAPI backend implementation

## Research Overview

This document consolidates technical research findings and decisions made during the planning phase for the Backend Todo API. All decisions align with the project constitution's principles of clean architecture, layer separation, and spec-driven development.

## Decision 1: UV Package Manager

**Context**: Need dependency management for Python project

**Question**: How to initialize and manage Python project with UV?

**Decision**: Use `uv init .`, `uv venv`, `uv add` workflow

**Rationale**:
- UV provides fast, reliable dependency management with automatic lock files
- Explicit user requirement in specification
- Modern tooling with better performance than pip
- Lock file ensures reproducible builds

**Alternatives Considered**:
1. **pip + venv**: Traditional approach
   - **Rejected**: Slower dependency resolution, no automatic lock file, manual requirements.txt management
2. **Poetry**: Popular Python dependency manager
   - **Rejected**: Not specified by user, different workflow, additional learning curve

**References**:
- UV Documentation: https://github.com/astral-sh/uv
- Lock file format ensures deterministic installs

**Implementation Notes**:
```bash
cd backend
uv init .           # Creates pyproject.toml
uv venv             # Creates .venv/
source .venv/bin/activate
uv add fastapi uvicorn pydantic
```

## Decision 2: FastAPI Project Structure

**Context**: Need maintainable code organization for API backend

**Question**: How to organize FastAPI routes, services, models for maintainability?

**Decision**: Adopt APIRouter pattern with separate route files, service layer for business logic, Pydantic models for validation

**Rationale**:
- Industry-standard pattern for FastAPI projects
- Enables clean separation of HTTP layer (routes) from business logic (services)
- Aligns with constitution's backend architecture principle (Principle III)
- Each layer has single responsibility
- Testable in isolation

**Architecture Pattern**:
```
Routes (HTTP) → Services (Business Logic) → Storage (In-Memory)
```

**Alternatives Considered**:
1. **Monolithic main.py**: All code in single file
   - **Rejected**: Doesn't scale beyond trivial apps, violates separation of concerns, hard to test
2. **Class-based views**: Django-style CBVs
   - **Rejected**: Less idiomatic for FastAPI, function-based views are simpler and more explicit

**References**:
- FastAPI Bigger Applications: https://fastapi.tiangolo.com/tutorial/bigger-applications/
- Pydantic Models: https://docs.pydantic.dev/latest/

**Implementation Structure**:
- `main.py`: App instance, router registration, startup/shutdown events
- `routes/todos.py`: APIRouter with all endpoints (thin controllers)
- `services/todo_service.py`: Business logic, validation, storage access
- `models/todo.py`: Pydantic models for request/response contracts

## Decision 3: In-Memory Storage Strategy

**Context**: Need todo persistence without database complexity

**Question**: Best approach for in-memory todo storage that meets spec requirements?

**Decision**: Module-level list `todos: List[dict]` in `todo_service.py` with auto-incrementing integer IDs

**Rationale**:
- Simplest solution that meets requirements
- No external dependencies (Redis, SQLite)
- Easy to test and debug
- Specification explicitly allows in-memory storage
- Constitution principle states "use simplest viable solution"
- Data loss on restart is acceptable per spec assumptions

**Storage Design**:
```python
todos: List[Dict] = []  # Module-level state
next_id: int = 1         # Auto-increment counter

# Each todo dict:
{
    "id": 1,
    "description": "Buy groceries",
    "completed": False,
    "created_at": "2025-12-28T10:30:00.123456",
    "updated_at": "2025-12-28T10:30:00.123456"
}
```

**Alternatives Considered**:
1. **Redis**: In-memory key-value store
   - **Rejected**: External dependency, over-engineering for MVP, requires Redis server
2. **SQLite in-memory mode**: SQL database in RAM
   - **Rejected**: Spec says "in-memory or simple file-based", SQLite adds SQL complexity
3. **Global dict keyed by ID**: `todos_dict: Dict[int, dict]`
   - **Rejected**: List is more natural for collections, iteration easier

**Concurrency Notes**:
- Global list is sufficient for single-process development server
- Python GIL provides basic thread safety for list operations
- No advanced locking needed for this phase
- Future phases can add proper concurrency control if needed

**References**:
- Spec Assumptions section: "In-memory storage is acceptable for this phase"

## Decision 4: Error Handling Pattern

**Context**: Need consistent error responses across all endpoints

**Question**: How to handle errors consistently in FastAPI?

**Decision**: Use HTTPException with appropriate status codes, raise from service layer when business rules violated

**Rationale**:
- FastAPI's built-in exception handler provides consistent JSON error responses
- Service layer can raise HTTPException directly (FastAPI import available everywhere)
- Automatic conversion to JSON response with proper status code
- No middleware or custom error handlers needed for simple API

**Error Flow**:
1. Pydantic validation errors → Automatic 422 (or 400 if configured)
2. Business rule violations → Service raises HTTPException with 400/404
3. Not found errors → Service raises HTTPException 404
4. Unexpected errors → FastAPI default handler returns 500

**Error Response Format** (FastAPI default):
```json
{
  "detail": "Error message here"
}
```

**Alternatives Considered**:
1. **Custom exception classes**: Define `TodoNotFoundError`, `InvalidTodoError`, etc.
   - **Rejected**: Over-engineering for 6 endpoints, adds unnecessary complexity
2. **Middleware error handler**: Global exception handler
   - **Rejected**: Not needed when HTTPException works well, adds indirection

**Implementation Example**:
```python
# In service layer:
def get_todo(todo_id: int) -> Dict:
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
```

**References**:
- FastAPI Error Handling: https://fastapi.tiangolo.com/tutorial/handling-errors/

## Decision 5: ID Generation Strategy

**Context**: Need unique identifiers for todos

**Question**: How to generate unique todo IDs that meet spec requirements?

**Decision**: Global counter variable `next_id`, increment on each create, thread-safe enough for development

**Rationale**:
- Spec requires integer IDs (not UUIDs)
- Auto-incrementing matches user expectations (IDs start at 1, increase sequentially)
- Simple, deterministic, easy to test
- No external dependencies
- Sufficient for single-process development server

**Implementation**:
```python
next_id: int = 1  # Module-level counter

def create_todo(description: str) -> Dict:
    global next_id
    todo = {
        "id": next_id,
        "description": description,
        # ... other fields
    }
    todos.append(todo)
    next_id += 1
    return todo
```

**Alternatives Considered**:
1. **UUID (Universal Unique Identifier)**: `uuid.uuid4()`
   - **Rejected**: Spec explicitly requires integer IDs, UUIDs are strings
2. **Hash-based IDs**: Hash of description + timestamp
   - **Rejected**: Unnecessary complexity, potential collisions, not sequential

**Thread Safety Notes**:
- Simple increment is atomic enough for development
- Python GIL provides basic protection
- No race conditions expected in single-process dev server
- Future: Use threading.Lock if multi-threading needed

## Decision 6: Timestamp Management

**Context**: Need created_at and updated_at timestamps per spec

**Question**: How to handle timestamps in UTC with proper formatting?

**Decision**: Use `datetime.utcnow()` from Python standard library, store as ISO 8601 strings, UTC timezone

**Rationale**:
- Standard library, no external dependencies
- ISO 8601 format is industry standard, human-readable, machine-parseable
- UTC avoids timezone complexity
- Pydantic automatically validates datetime strings

**Implementation**:
```python
from datetime import datetime

todo = {
    "created_at": datetime.utcnow().isoformat(),  # "2025-12-28T10:30:00.123456"
    "updated_at": datetime.utcnow().isoformat()
}
```

**Alternatives Considered**:
1. **Unix timestamps (integers)**: Seconds since epoch
   - **Rejected**: Less human-readable, requires conversion for display
2. **Timezone-aware datetimes**: Include timezone info
   - **Rejected**: Added complexity, spec says UTC is acceptable, ISO string sufficient

**Pydantic Integration**:
```python
class TodoResponse(BaseModel):
    created_at: datetime  # Pydantic auto-converts ISO string to datetime object
    updated_at: datetime
```

**References**:
- ISO 8601 Standard: https://en.wikipedia.org/wiki/ISO_8601
- Spec Assumptions: "UTC timezone for all timestamps"

## Summary of Key Decisions

| Decision | Choice | Primary Rationale |
|----------|--------|-------------------|
| Package Manager | UV (uv init, uv venv, uv add) | User requirement, fast, lock files |
| Project Structure | Routes → Services → Storage | Clean architecture, testability |
| Storage | In-memory list with dicts | Simplest solution, meets spec |
| Error Handling | HTTPException from FastAPI | Consistent JSON, built-in support |
| ID Generation | Auto-increment integer | Spec requirement, simple, deterministic |
| Timestamps | datetime.utcnow().isoformat() | Standard library, ISO 8601, UTC |

## Implementation Readiness

All technical unknowns have been resolved. The decisions above provide:
- ✅ Clear implementation path for all 5 implementation phases
- ✅ No external services required (no Redis, no database)
- ✅ Minimal dependencies (FastAPI, Uvicorn, Pydantic)
- ✅ Alignment with constitution principles
- ✅ Simplicity and testability
- ✅ Meets all spec requirements

**Next Phase**: Proceed to Phase 1 (Data Model, API Contracts, Quickstart Guide)
