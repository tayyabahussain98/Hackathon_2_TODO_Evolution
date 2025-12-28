# Data Model: CLI Todo Core Application

**Feature**: 001-cli-todo-core
**Date**: 2025-12-27
**Status**: Complete

## Entities

### Task

The single entity in this application representing a todo item.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | int | Positive integer, unique, auto-assigned | Unique identifier for the task |
| description | str | Non-empty string | Text describing the task |
| completed | bool | Default: False | Whether the task is done |

**Validation Rules**:
- `id` MUST be a positive integer (> 0)
- `id` MUST be unique across all tasks
- `id` is auto-assigned by the system (max existing + 1, or 1 if empty)
- `id` is never reused after deletion
- `description` MUST be a non-empty string after stripping whitespace
- `completed` defaults to `False` when task is created

**State Transitions**:

```
[Created] → completed=False
    ↓
[Complete Command] → toggles completed
    ↓
completed=True ↔ completed=False (toggle on each complete command)
```

## Storage Schema

### tasks.json

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["id", "description", "completed"],
    "properties": {
      "id": {
        "type": "integer",
        "minimum": 1,
        "description": "Unique task identifier"
      },
      "description": {
        "type": "string",
        "minLength": 1,
        "description": "Task description text"
      },
      "completed": {
        "type": "boolean",
        "description": "Task completion status"
      }
    },
    "additionalProperties": false
  }
}
```

**Example**:
```json
[
  {"id": 1, "description": "Buy groceries", "completed": false},
  {"id": 2, "description": "Call dentist", "completed": true},
  {"id": 3, "description": "Finish report", "completed": false}
]
```

**File Behavior**:
- Created automatically on first task addition if not exists
- Empty array `[]` represents no tasks
- File is overwritten on each operation (not appended)
- Invalid JSON triggers error message without data loss

## Python Implementation

### Dataclass Definition (src/models.py)

```python
from dataclasses import dataclass

@dataclass
class Task:
    """Represents a single todo item."""
    id: int
    description: str
    completed: bool = False
```

### Serialization (src/storage.py)

```python
# Task to dict (for JSON)
{"id": task.id, "description": task.description, "completed": task.completed}

# Dict to Task (from JSON)
Task(id=d["id"], description=d["description"], completed=d["completed"])
```

## Relationships

This is a single-entity model with no relationships. Tasks are independent of each other.

## Indexes

Not applicable - file-based storage. Linear search by ID is acceptable for scale (up to 1000 tasks).
