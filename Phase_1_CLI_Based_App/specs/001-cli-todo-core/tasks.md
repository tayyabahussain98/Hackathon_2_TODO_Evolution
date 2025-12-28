# Tasks: CLI Todo Core Application

**Input**: Design documents from `/specs/001-cli-todo-core/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/cli-commands.md

**Tests**: Not requested in feature specification. Tests are NOT included per constitution architecture.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/` at repository root (per constitution)
- `main.py` in root for CLI entry point
- `tasks.json` in root for storage (auto-generated)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize Python project with UV in current directory using `uv init .`
- [x] T002 Create virtual environment using `uv venv` and add rich dependency using `uv add rich`
- [x] T003 Create src/ directory structure with `__init__.py` package marker

**Checkpoint**: Project structure ready for foundational code

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create Task dataclass in src/models.py with id, description, completed fields per data-model.md
- [x] T005 [P] Implement load_tasks() function in src/storage.py to read tasks from tasks.json
- [x] T006 [P] Implement save_tasks() function in src/storage.py to write tasks to tasks.json
- [x] T007 Create base UI helper functions in src/ui.py: display_error(), display_success(), display_help()
- [x] T008 [P] Implement display_task_table() function in src/ui.py using rich Table for formatted output
- [x] T009 Create main.py CLI entry point with argument parsing and command routing skeleton
- [x] T010 Implement help command output in main.py per contracts/cli-commands.md
- [x] T011 Implement unknown command error handling in main.py per contracts/cli-commands.md

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Add New Task (Priority: P1)

**Goal**: Users can add new tasks via `uv run main.py add "description"`

**Independent Test**: Run `uv run main.py add "Test task"` and verify task appears in tasks.json and confirmation displays

### Implementation for User Story 1

- [x] T012 [US1] Implement add_task() service function in src/services.py with ID generation and validation
- [x] T013 [US1] Implement display_add_success() UI function in src/ui.py per contracts/cli-commands.md
- [x] T014 [US1] Implement display_add_error() UI function in src/ui.py for empty description error
- [x] T015 [US1] Wire add command in main.py: parse args, call service, display result

**Checkpoint**: User Story 1 complete - users can add tasks and see formatted confirmation

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Users can view all tasks in formatted table via `uv run main.py list`

**Independent Test**: Add tasks, run `uv run main.py list`, verify formatted table with ID, Description, Status columns

### Implementation for User Story 2

- [x] T016 [US2] Implement list_tasks() service function in src/services.py (returns all tasks)
- [x] T017 [US2] Implement display_task_list() UI function in src/ui.py with empty list message per contracts/cli-commands.md
- [x] T018 [US2] Wire list command in main.py: call service, display formatted table

**Checkpoint**: User Stories 1 AND 2 complete - MVP functional (add + view)

---

## Phase 5: User Story 3 - Mark Task Complete (Priority: P2)

**Goal**: Users can toggle task completion via `uv run main.py complete <id>`

**Independent Test**: Add task, run `uv run main.py complete 1`, verify status toggles and confirmation displays

### Implementation for User Story 3

- [x] T019 [US3] Implement complete_task() service function in src/services.py with toggle logic and not-found handling
- [x] T020 [US3] Implement display_complete_success() UI function in src/ui.py per contracts/cli-commands.md
- [x] T021 [US3] Implement display_task_not_found() UI function in src/ui.py (shared error for US3, US4, US5)
- [x] T022 [US3] Implement display_invalid_id() UI function in src/ui.py (shared error for US3, US4, US5)
- [x] T023 [US3] Wire complete command in main.py: parse ID, validate, call service, display result

**Checkpoint**: User Story 3 complete - users can track task progress

---

## Phase 6: User Story 4 - Update Task Description (Priority: P3)

**Goal**: Users can update task descriptions via `uv run main.py update <id> "new description"`

**Independent Test**: Add task, run `uv run main.py update 1 "Updated"`, verify description changes and before/after displays

### Implementation for User Story 4

- [x] T024 [US4] Implement update_task() service function in src/services.py with validation and not-found handling
- [x] T025 [US4] Implement display_update_success() UI function in src/ui.py with before/after per contracts/cli-commands.md
- [x] T026 [US4] Wire update command in main.py: parse ID and description, validate, call service, display result

**Checkpoint**: User Story 4 complete - users can edit tasks

---

## Phase 7: User Story 5 - Delete Task (Priority: P3)

**Goal**: Users can remove tasks via `uv run main.py delete <id>`

**Independent Test**: Add task, run `uv run main.py delete 1`, verify task removed from list

### Implementation for User Story 5

- [x] T027 [US5] Implement delete_task() service function in src/services.py with not-found handling
- [x] T028 [US5] Implement display_delete_success() UI function in src/ui.py per contracts/cli-commands.md
- [x] T029 [US5] Wire delete command in main.py: parse ID, validate, call service, display result

**Checkpoint**: User Story 5 complete - all 5 core operations functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and cleanup

- [x] T030 Validate all commands against quickstart.md workflow
- [x] T031 Verify edge cases: corrupted JSON handling, missing file creation, negative IDs
- [x] T032 Final code review: type hints, docstrings, PEP 8 compliance per constitution

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - US1 (Add) and US2 (List) can run in parallel after Foundational
  - US3 (Complete), US4 (Update), US5 (Delete) depend on US1+US2 conceptually but files are independent
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundational - Uses shared UI functions from US3 (T021, T022)
- **User Story 4 (P3)**: Can start after US3 complete - Reuses T021, T022 error UI functions
- **User Story 5 (P3)**: Can start after US3 complete - Reuses T021, T022 error UI functions

### Within Each User Story

- Services before UI (service functions needed for UI to display results)
- UI before main.py wiring (UI functions needed for command handlers)
- Each story complete before moving to next priority

### Parallel Opportunities

- T005 and T006 can run in parallel (different functions in same file, no dependencies)
- T007 and T008 can run in parallel (different functions in same file)
- US1 (T012-T015) and US2 (T016-T018) can run in parallel after Foundational
- US4 and US5 can run in parallel after US3 (both reuse error functions)

---

## Parallel Example: Foundational Phase

```bash
# Launch these storage functions in parallel:
Task: "T005 Implement load_tasks() in src/storage.py"
Task: "T006 Implement save_tasks() in src/storage.py"

# Launch these UI functions in parallel:
Task: "T007 Create base UI helpers in src/ui.py"
Task: "T008 Implement display_task_table() in src/ui.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T011)
3. Complete Phase 3: User Story 1 - Add (T012-T015)
4. Complete Phase 4: User Story 2 - List (T016-T018)
5. **STOP and VALIDATE**: Users can add and view tasks
6. Demo MVP if ready

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add User Story 1 (Add) → Test independently
3. Add User Story 2 (List) → Test independently → **MVP Complete!**
4. Add User Story 3 (Complete) → Test independently
5. Add User Story 4 (Update) → Test independently
6. Add User Story 5 (Delete) → Test independently
7. Polish phase → Final validation

### Single Developer Strategy (Recommended)

Execute tasks in order T001 → T032:
1. Phase 1: Setup (T001-T003)
2. Phase 2: Foundational (T004-T011)
3. Phase 3-7: User Stories in priority order
4. Phase 8: Polish

---

## Summary

| Metric | Value |
|--------|-------|
| Total Tasks | 32 |
| Setup Tasks | 3 |
| Foundational Tasks | 8 |
| US1 (Add) Tasks | 4 |
| US2 (List) Tasks | 3 |
| US3 (Complete) Tasks | 5 |
| US4 (Update) Tasks | 3 |
| US5 (Delete) Tasks | 3 |
| Polish Tasks | 3 |
| Parallel Opportunities | 6 groups |
| MVP Scope | T001-T018 (18 tasks) |

---

## Notes

- [P] tasks = different files or independent functions, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Constitution mandates: type hints, docstrings, PEP 8, no globals
