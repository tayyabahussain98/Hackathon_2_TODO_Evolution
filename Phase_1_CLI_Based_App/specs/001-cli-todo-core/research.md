# Research: CLI Todo Core Application

**Feature**: 001-cli-todo-core
**Date**: 2025-12-27
**Status**: Complete

## Research Tasks

No NEEDS CLARIFICATION items were identified in the Technical Context. The constitution provides all necessary technical decisions. This document captures best practices research for the chosen technologies.

## Technology Decisions

### 1. Python CLI Argument Parsing

**Decision**: Use `sys.argv` with manual parsing

**Rationale**:
- Constitution specifies minimal dependencies (standard library + rich only)
- argparse adds complexity for 5 simple commands
- Manual parsing provides full control over command syntax
- Keeps main.py simple and readable

**Alternatives Considered**:
- `argparse`: Overkill for 5 commands with simple signatures; adds boilerplate
- `click`: External dependency, violates constitution's minimal dependency rule
- `typer`: External dependency, violates constitution's minimal dependency rule

### 2. JSON Storage Format

**Decision**: List of task dictionaries with auto-incrementing ID

**Rationale**:
- Simple, human-readable format
- Easy to load/save with standard library `json` module
- Natural mapping to Python list of dataclasses

**Format**:
```json
[
  {"id": 1, "description": "Buy groceries", "completed": false},
  {"id": 2, "description": "Call dentist", "completed": true}
]
```

**Alternatives Considered**:
- Dictionary keyed by ID: Slightly more efficient for lookups but less intuitive format
- SQLite: External database, violates constitution's "no external databases" rule
- YAML: Requires external library, violates minimal dependency rule

### 3. Task ID Generation

**Decision**: Sequential integers, never reused after deletion

**Rationale**:
- Per spec assumption: "Task IDs are sequential integers and not reused after deletion"
- Simple to implement: max(existing_ids) + 1 or 1 if empty
- Prevents confusion if user references recently deleted ID

**Implementation**:
```python
def next_id(tasks: list[Task]) -> int:
    if not tasks:
        return 1
    return max(task.id for task in tasks) + 1
```

### 4. Rich Library Usage Patterns

**Decision**: Use Console, Table, and Panel components

**Rationale**:
- Constitution requires "website-like" CLI experience
- Rich provides all needed components in one library
- Well-documented, actively maintained

**Components to Use**:
- `Console`: Central output handler with print method
- `Table`: Formatted task list display with columns
- `Panel`: Bordered messages for confirmations and errors
- Icons: Unicode characters (checkmark, cross, etc.)

**Best Practices**:
- Create single Console instance in ui.py
- Use consistent color scheme (green=success, red=error, yellow=warning)
- Use emoji/unicode icons for visual feedback

### 5. Error Handling Strategy

**Decision**: Graceful error handling with user-friendly messages

**Rationale**:
- Per FR-011: "System MUST display helpful error messages"
- Per edge case: "exits gracefully without data loss"

**Error Categories**:
| Error Type | Handling |
|------------|----------|
| Task not found | Display error with ID, suggest `list` command |
| Invalid ID format | Display error explaining ID must be positive integer |
| Empty description | Display error explaining description is required |
| Corrupted JSON | Display error, do not overwrite file |
| File not found | Create empty tasks.json on first write |

### 6. Module Responsibility Boundaries

**Decision**: Strict separation per constitution

**Rationale**:
- Constitution defines exact module responsibilities
- Enables independent testing and clear ownership

**Boundaries**:
| Module | Allowed | Not Allowed |
|--------|---------|-------------|
| models.py | Dataclass definition, validation | I/O, UI, business logic |
| services.py | CRUD logic, ID generation | I/O, UI |
| storage.py | File read/write, JSON parsing | Business logic, UI |
| ui.py | Console output, formatting | Business logic, I/O |
| main.py | Orchestration, arg parsing | Business logic |

## Resolved Clarifications

All technical decisions were pre-determined by the constitution. No clarifications needed.

## References

- [Rich Documentation](https://rich.readthedocs.io/)
- [Python Dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [JSON Module](https://docs.python.org/3/library/json.html)
- [UV Package Manager](https://github.com/astral-sh/uv)
