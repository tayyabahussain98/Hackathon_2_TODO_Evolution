# Tasks: Backend Todo API

**Input**: Design documents from `/specs/001-backend-todo-api/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/openapi.yaml ✅, quickstart.md ✅

**Tests**: Manual testing via curl/Postman as specified in quickstart.md. No automated tests in this phase.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Web app backend**: `backend/` folder containing all FastAPI code
- Backend structure: `backend/{main.py, routes/, services/, models/, core/}`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend/ folder and initialize UV project with `uv init .`
- [x] T002 Create Python virtual environment with `uv venv` and activate it
- [x] T003 Install FastAPI dependencies: `uv add fastapi uvicorn pydantic`
- [x] T004 [P] Create directory structure: backend/routes/, backend/services/, backend/models/, backend/core/
- [x] T005 [P] Create __init__.py files in backend/routes/, backend/services/, backend/models/, backend/core/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 [P] Create Pydantic models in backend/models/todo.py (TodoCreate, TodoUpdate, TodoResponse)
- [x] T007 [P] Create configuration settings in backend/core/config.py with app_name, port, log_level
- [x] T008 Initialize in-memory storage in backend/services/todo_service.py (todos list, next_id counter)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and View Todos (Priority: P1) 🎯 MVP

**Goal**: Enable API clients to create todos and retrieve them via REST endpoints

**Independent Test**: POST to create todos, GET to list all, GET by ID to retrieve specific todo. Test completely independently without other user stories.

### Implementation for User Story 1

- [x] T009 [P] [US1] Implement create_todo() in backend/services/todo_service.py with ID generation and timestamps
- [x] T010 [P] [US1] Implement list_todos() in backend/services/todo_service.py returning all todos
- [x] T011 [P] [US1] Implement get_todo(todo_id) in backend/services/todo_service.py with 404 handling
- [x] T012 [US1] Create APIRouter in backend/routes/todos.py with prefix="/api/todos"
- [x] T013 [US1] Implement POST /api/todos endpoint in backend/routes/todos.py (status 201, calls create_todo)
- [x] T014 [US1] Implement GET /api/todos endpoint in backend/routes/todos.py (status 200, calls list_todos)
- [x] T015 [US1] Implement GET /api/todos/{id} endpoint in backend/routes/todos.py (status 200 or 404, calls get_todo)
- [x] T016 [US1] Create FastAPI app instance in backend/main.py and include todos router
- [x] T017 [US1] Test US1: Create todo via POST, list all via GET, get by ID via GET (verify 201, 200, 404 responses)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Can create and view todos.

---

## Phase 4: User Story 4 - Health Check Monitoring (Priority: P1) 🎯 MVP

**Goal**: Provide health check endpoint for deployment and monitoring infrastructure

**Independent Test**: GET /health returns 200 with {"status": "healthy"} in under 100ms

### Implementation for User Story 4

- [x] T018 [US4] Implement GET /health endpoint in backend/main.py returning {"status": "healthy"}
- [x] T019 [US4] Test US4: Verify GET /health returns 200 with correct JSON response

**Checkpoint**: At this point, User Stories 1 AND 4 should both work independently. This is the MVP.

---

## Phase 5: User Story 2 - Update Todo Status (Priority: P2)

**Goal**: Enable API clients to update todo items (description or completion status)

**Independent Test**: Create a todo, then PATCH to change description or toggle completion status. Verify updated_at changes.

### Implementation for User Story 2

- [x] T020 [US2] Implement update_todo(todo_id, description, completed) in backend/services/todo_service.py with timestamp refresh
- [x] T021 [US2] Implement PATCH /api/todos/{id} endpoint in backend/routes/todos.py (status 200 or 404, calls update_todo)
- [x] T022 [US2] Test US2: Create todo, PATCH description only, PATCH completed only, PATCH both fields, verify 400 for empty description

**Checkpoint**: At this point, User Stories 1, 4, AND 2 should all work independently. Can create, view, and update todos.

---

## Phase 6: User Story 3 - Delete Todos (Priority: P3)

**Goal**: Enable API clients to delete todo items for cleanup

**Independent Test**: Create a todo, DELETE it, verify 204 response and subsequent GET returns 404

### Implementation for User Story 3

- [x] T023 [US3] Implement delete_todo(todo_id) in backend/services/todo_service.py with 404 handling
- [x] T024 [US3] Implement DELETE /api/todos/{id} endpoint in backend/routes/todos.py (status 204 or 404, calls delete_todo)
- [x] T025 [US3] Test US3: Create todo, DELETE it (verify 204), attempt GET/PATCH/DELETE again (verify all return 404)

**Checkpoint**: All user stories should now be independently functional. Full CRUD operations available.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T026 [P] Add logging configuration in backend/main.py with basicConfig (INFO level, timestamp format)
- [x] T027 [P] Add startup and shutdown event handlers in backend/main.py with log messages
- [x] T028 Run complete end-to-end workflow test per quickstart.md (health → create 2 todos → list → get → update → delete)
- [x] T029 Verify all 8 success criteria from spec.md are met
- [x] T030 Validate quickstart.md instructions work from scratch

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P1 → P2 → P3)
  - **MVP = US1 + US4** (P1 stories only)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories (independent endpoint)
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Uses same service layer as US1 but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Uses same service layer as US1 but independently testable

### Within Each User Story

- Service functions before route handlers
- All endpoints for a story before testing
- Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1**: T004 and T005 can run in parallel (different directories)
- **Phase 2**: T006, T007, and T008 can run in parallel (different files)
- **Phase 3 (US1)**: T009, T010, T011 can run in parallel (same file but different functions)
- **Phase 4 (US4)**: Can run in parallel with US1 implementation (different endpoints)
- **Phase 7**: T026 and T027 can run in parallel (different sections of main.py)

---

## Parallel Example: User Story 1

```bash
# Launch all service functions for User Story 1 together:
Task T009: "Implement create_todo() in backend/services/todo_service.py"
Task T010: "Implement list_todos() in backend/services/todo_service.py"
Task T011: "Implement get_todo(todo_id) in backend/services/todo_service.py"
```

---

## Parallel Example: MVP (US1 + US4)

```bash
# After Foundational phase completes, work on both P1 stories simultaneously:
Developer A: Complete Phase 3 (User Story 1 - Create and View Todos)
Developer B: Complete Phase 4 (User Story 4 - Health Check)
# Result: MVP delivered with both P1 stories complete
```

---

## Implementation Strategy

### MVP First (User Stories 1 and 4 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T008) - CRITICAL, blocks all stories
3. Complete Phase 3: User Story 1 (T009-T017)
4. Complete Phase 4: User Story 4 (T018-T019)
5. **STOP and VALIDATE**: Test both US1 and US4 independently
6. Deploy/demo MVP if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 + User Story 4 → Test independently → Deploy/Demo (MVP with P1 features!)
3. Add User Story 2 → Test independently → Deploy/Demo (adds update capability)
4. Add User Story 3 → Test independently → Deploy/Demo (adds delete capability)
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T008)
2. Once Foundational is done:
   - Developer A: User Story 1 (T009-T017)
   - Developer B: User Story 4 (T018-T019)
   - Developer C: User Story 2 (T020-T022)
   - Developer D: User Story 3 (T023-T025)
3. Stories complete and integrate independently
4. Polish phase (T026-T030) done together

---

## Task Count Summary

- **Total Tasks**: 30
- **Setup**: 5 tasks
- **Foundational**: 3 tasks (CRITICAL PATH)
- **User Story 1 (P1)**: 9 tasks (MVP)
- **User Story 4 (P1)**: 2 tasks (MVP)
- **User Story 2 (P2)**: 3 tasks
- **User Story 3 (P3)**: 3 tasks
- **Polish**: 5 tasks

**MVP Scope**: 19 tasks total (Setup + Foundational + US1 + US4)

**Parallel Opportunities**: 8 tasks marked [P] can run in parallel with others

---

## Notes

- [P] tasks = different files or functions, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Manual testing via curl or FastAPI /docs interface (no pytest in this phase)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- MVP = US1 + US4 (both P1 priorities) = 11 implementation tasks
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
