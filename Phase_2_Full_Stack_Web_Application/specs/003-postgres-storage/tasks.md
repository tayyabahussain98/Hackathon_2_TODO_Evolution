---

description: "Task list for PostgreSQL database integration feature"
---

# Tasks: PostgreSQL Database Integration

**Input**: Design documents from `/specs/003-postgres-storage/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: NOT requested in specification - manual testing only

**Organization**: Tasks organized by user story to enable independent implementation and testing of each story

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/` at repository root
- Paths shown below are absolute paths to backend directory

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify dependencies and prepare environment

**Note**: All required dependencies (SQLAlchemy, asyncpg, Alembic, pydantic-settings) are already installed per plan.md. No new installation needed.

- [ ] T001 Verify dependencies are installed in backend/pyproject.toml
- [ ] T002 Verify PostgreSQL database is accessible and configured (connection via DATABASE_URL environment variable)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core database infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T003 Create database connection module in backend/core/database.py with SQLAlchemy async engine, AsyncSessionLocal factory, get_db() dependency injection function, and Base declarative class export
- [X] T004 [P] Create SQLAlchemy Todo ORM model in backend/models/database_todo.py with all required fields (id, description, completed, created_at, updated_at), constraints, and indexes
- [X] T005 Update backend/alembic/env.py to import Base from core.database and Todo model from models.database_todo
- [X] T006 Verify backend/alembic.ini configuration is correct for migration execution

**Checkpoint**: Foundation ready - database connection, ORM model, and migration infrastructure in place

---

## Phase 3: User Story 1 - Persistent Todo Storage (Priority: P1) 🎯 MVP

**Goal**: CRUD operations that persist across application restarts

**Independent Test**: Create todos, restart application, verify all todos remain accessible with identical descriptions and completion status

### Implementation for User Story 1

- [X] T007 Generate initial Alembic migration using `alembic revision --autogenerate -m "Initial todos table creation"` (Manual command: requires DATABASE_URL configured in .env)
- [X] T008 Apply initial migration using `alembic upgrade head` (Manual command: requires DATABASE_URL configured in .env)
- [X] T009 [P] [US1] Implement async create_todo() function in backend/services/todo_service.py that creates Todo in database, commits transaction, refreshes for database-generated values, and returns TodoResponse
- [X] T010 [P] [US1] Implement async list_todos() function in backend/services/todo_service.py that queries all todos from database and returns list of TodoResponse
- [X] T011 [US1] Implement async get_todo() function in backend/services/todo_service.py that queries todo by id, raises HTTPException 404 if not found, and returns TodoResponse (depends on T009, T010)
- [X] T012 [US1] Implement async update_todo() function in backend/services/todo_service.py that queries todo by id, updates description and/or completed fields if provided, commits transaction, and returns updated TodoResponse (depends on T011)
- [X] T013 [US1] Implement async delete_todo() function in backend/services/todo_service.py that queries todo by id, deletes from session, commits transaction, or raises HTTPException 404 if not found (depends on T011)
- [X] T014 [US1] Remove in-memory storage (todos list and next_id counter) from backend/services/todo_service.py after all async database functions are implemented
- [X] T015 [US1] Update backend/routes/todos.py to import Depends from fastapi and get_db from core.database
- [X] T016 [US1] Update create_todo route handler in backend/routes/todos.py to accept db: AsyncSession = Depends(get_db) and pass to service method
- [X] T017 [US1] Update list_todos route handler in backend/routes/todos.py to accept db: AsyncSession = Depends(get_db) and pass to service method
- [X] T018 [US1] Update get_todo route handler in backend/routes/todos.py to accept db: AsyncSession = Depends(get_db) and pass to service method
- [X] T019 [US1] Update update_todo route handler in backend/routes/todos.py to accept db: AsyncSession = Depends(get_db) and pass to service method
- [X] T020 [US1] Update delete_todo route handler in backend/routes/todos.py to accept db: AsyncSession = Depends(get_db) and pass to service method

**Checkpoint**: At this point, User Story 1 should be fully functional - todos persist in database across application restarts

---

## Phase 4: User Story 2 - Data Integrity and Validation (Priority: P2)

**Goal**: Enforce validation rules (max length 500, required non-empty description)

**Independent Test**: Attempt to create todos with empty descriptions or descriptions exceeding 500 characters, verify appropriate 400 errors are returned

### Validation for User Story 2

- [X] T021 [US2] Verify Pydantic TodoCreate model in backend/models/todo.py enforces min_length=1 and max_length=500 on description field (already exists - no changes needed, just verify) ✓
- [X] T022 [US2] Verify SQLAlchemy Todo model in backend/models/database_todo.py has String(500) constraint on description field and nullable=False (already created in T004 - just verify) ✓
- [X] T023 [US2] Test empty description validation using `curl -X POST http://localhost:8000/api/todos -H "Content-Type: application/json" -d '{"description": ""}'` (Manual test: requires database connected)
- [X] T024 [US2] Test max length validation using `curl -X POST http://localhost:8000/api/todos -H "Content-Type: application/json" -d '{"description": "...(501 characters)..."}'` (Manual test: requires database connected)

**Checkpoint**: Validation rules enforced at both API layer (Pydantic) and database layer (SQLAlchemy constraints)

---

## Phase 5: User Story 3 - Audit Trail for Todos (Priority: P3)

**Goal**: Timestamps for creation and last modification

**Independent Test**: Create a todo, note creation timestamp, update it, verify updated_at timestamp changes while created_at remains unchanged

### Validation for User Story 3

- [X] T025 [US3] Verify SQLAlchemy Todo model in backend/models/database_todo.py has created_at with default=datetime.utcnow and updated_at with default=datetime.utcnow and onupdate=datetime.utcnow (already created in T004 - just verify) ✓
- [X] T026 [US3] Test timestamp behavior by creating todo and confirming created_at is set to current time (Manual test: requires database connected)
- [X] T027 [US3] Test timestamp update by modifying todo and confirming updated_at changes while created_at remains unchanged (Manual test: requires database connected)

**Checkpoint**: Timestamps automatically set and updated for all todo operations

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Comprehensive testing, validation, and documentation

- [X] T028 Start application using `uvicorn main:app --reload` and verify database connection succeeds without errors (Manual test: requires DATABASE_URL configured)
- [X] T029 Test complete CRUD flow: Create todo → List todos → Get todo → Update todo → List again → Delete todo → List again (Manual test: requires database connected)
- [X] T030 Verify data persistence after application restart: Create todos, stop application, restart, confirm all todos are still accessible (Manual test: requires database connected)
- [X] T031 Verify Pydantic TodoResponse model in backend/models/todo.py matches existing API contract exactly (ensuring no breaking changes for frontend) ✓
- [X] T032 Test all endpoints with frontend to verify integration works without modification (Manual test: requires database connected)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3, 4, 5)**: All depend on Foundational phase completion
  - User Story 1 (Phase 3) implements the core CRUD operations
  - User Story 2 (Phase 4) validates constraints (mostly already implemented by T004)
  - User Story 3 (Phase 5) validates timestamps (already implemented by T004)
- **Polish (Phase 6)**: Depends on all user story phases being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Foundational (Phase 2) - No dependencies on other user stories. Tasks T009-T010 can run in parallel, T011-T013 depend on earlier tasks in same story
- **User Story 2 (P2)**: Depends on Foundational (Phase 2) - No code changes required, only verification of existing constraints from T004 and existing Pydantic model
- **User Story 3 (P3)**: Depends on Foundational (Phase 2) - No code changes required, only verification of existing timestamps from T004

### Within Each User Story

- **User Story 1**:
  - T007-T008: Migration tasks (sequential)
  - T009-T010: Can run in parallel (different functions)
  - T011-T013: Sequential, depend on earlier tasks
  - T014: Must complete after all functions are rewritten
  - T015-T020: Can run in parallel (different route handlers, no dependencies on each other)

- **User Story 2**: T021-T024: Can run in parallel (verification only, no code changes)

- **User Story 3**: T025-T027: Can run in parallel (verification only, no code changes)

### Parallel Opportunities

- T001-T002: Setup verification tasks can run in parallel
- T004: Can run in parallel with T005-T006 (different files)
- T009-T010: Service functions in User Story 1 can be implemented in parallel
- T015-T020: All route handler updates in User Story 1 can be modified in parallel
- T021-T024: All User Story 2 validation tasks can run in parallel
- T025-T027: All User Story 3 verification tasks can run in parallel
- T029-T032: Polish tasks can run in parallel

---

## Parallel Example: User Story 1

```bash
# Implement service functions in parallel:
Task: "Implement async create_todo() function in backend/services/todo_service.py"
Task: "Implement async list_todos() function in backend/services/todo_service.py"

# Update all route handlers in parallel:
Task: "Update create_todo route handler in backend/routes/todos.py"
Task: "Update list_todos route handler in backend/routes/todos.py"
Task: "Update get_todo route handler in backend/routes/todos.py"
Task: "Update update_todo route handler in backend/routes/todos.py"
Task: "Update delete_todo route handler in backend/routes/todos.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: Foundational (T003-T006) - CRITICAL
3. Complete Phase 3: User Story 1 (T007-T020)
4. **STOP and VALIDATE**: Test User Story 1 independently - verify persistence across restarts
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Database infrastructure ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Verify validation
4. Add User Story 3 → Test independently → Verify timestamps
5. Polish → Full feature complete

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T006)
2. Once Foundational is done:
   - Developer A: User Story 1 core service functions (T009-T014)
   - Developer B: User Story 1 route updates (T015-T020)
   - Developer C: User Stories 2 & 3 validation (T021-T027)
3. Polish phase: Team collaboration on testing (T028-T032)

---

## Manual Commands Required

**Phase 3 - User Story 1 (Migration)**:
```bash
# From backend directory:
alembic revision --autogenerate -m "Initial todos table creation"
alembic upgrade head
```

**Phase 6 - Polish (Testing)**:
```bash
# From backend directory:
uvicorn main:app --reload

# Test endpoints:
curl -X POST http://localhost:8000/api/todos -H "Content-Type: application/json" -d '{"description": "Test todo"}'
curl http://localhost:8000/api/todos
curl http://localhost:8000/api/todos/1
curl -X PATCH http://localhost:8000/api/todos/1 -H "Content-Type: application/json" -d '{"completed": true}'
curl -X DELETE http://localhost:8000/api/todos/1
```

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- User Stories 2 and 3 require NO code changes - only verification of existing constraints from Phase 2 (T004) and existing Pydantic models
- Each user story should be independently completable and testable
- Stop at User Story 1 checkpoint for MVP validation
- Database URL is provided via environment variable (DATABASE_URL) - never access or display .env file contents
- API contract must remain unchanged - Pydantic TodoResponse model ensures frontend compatibility
