# CLI Command Contracts: CLI Todo Core Application

**Feature**: 001-cli-todo-core
**Date**: 2025-12-27
**Status**: Complete

## Command Overview

| Command | Syntax | Description |
|---------|--------|-------------|
| add | `uv run main.py add "<description>"` | Add new task |
| list | `uv run main.py list` | Display all tasks |
| complete | `uv run main.py complete <id>` | Toggle task completion |
| update | `uv run main.py update <id> "<description>"` | Update task description |
| delete | `uv run main.py delete <id>` | Remove task |
| (none) | `uv run main.py` | Display help |
| (invalid) | `uv run main.py <unknown>` | Display error + help |

---

## Command: add

**Syntax**: `uv run main.py add "<description>"`

**Input**:
- `description` (string, required): Non-empty task description

**Output (Success)**:
```
✅ Task added successfully!
┌─────┬─────────────────┬────────┐
│ ID  │ Description     │ Status │
├─────┼─────────────────┼────────┤
│ 1   │ Buy groceries   │ ☐      │
└─────┴─────────────────┴────────┘
```

**Output (Error - Empty Description)**:
```
❌ Error: Description cannot be empty.
Usage: uv run main.py add "<description>"
```

**Behavior**:
1. Validate description is non-empty after stripping whitespace
2. Generate next available ID
3. Create Task with completed=False
4. Save to tasks.json
5. Display confirmation with task details

**Exit Codes**:
- 0: Success
- 1: Validation error

---

## Command: list

**Syntax**: `uv run main.py list`

**Input**: None

**Output (With Tasks)**:
```
📋 Your Tasks
┌─────┬─────────────────┬────────┐
│ ID  │ Description     │ Status │
├─────┼─────────────────┼────────┤
│ 1   │ Buy groceries   │ ☐      │
│ 2   │ Call dentist    │ ☑      │
│ 3   │ Finish report   │ ☐      │
└─────┴─────────────────┴────────┘
```

**Output (No Tasks)**:
```
📋 Your Tasks
No tasks yet! Add one with: uv run main.py add "<description>"
```

**Behavior**:
1. Load tasks from tasks.json (or empty list if file doesn't exist)
2. Display formatted table with all tasks
3. Show ☑ for completed, ☐ for pending

**Exit Codes**:
- 0: Success (always)

---

## Command: complete

**Syntax**: `uv run main.py complete <id>`

**Input**:
- `id` (integer, required): Task ID to toggle

**Output (Success - Now Completed)**:
```
✅ Task marked as complete!
┌─────┬─────────────────┬────────┐
│ ID  │ Description     │ Status │
├─────┼─────────────────┼────────┤
│ 1   │ Buy groceries   │ ☑      │
└─────┴─────────────────┴────────┘
```

**Output (Success - Now Pending)**:
```
✅ Task marked as pending!
┌─────┬─────────────────┬────────┐
│ ID  │ Description     │ Status │
├─────┼─────────────────┼────────┤
│ 1   │ Buy groceries   │ ☐      │
└─────┴─────────────────┴────────┘
```

**Output (Error - Not Found)**:
```
❌ Error: Task with ID 99 not found.
Use 'uv run main.py list' to see all tasks.
```

**Output (Error - Invalid ID)**:
```
❌ Error: ID must be a positive integer.
Usage: uv run main.py complete <id>
```

**Behavior**:
1. Validate ID is positive integer
2. Find task by ID
3. Toggle completed status
4. Save to tasks.json
5. Display confirmation with new status

**Exit Codes**:
- 0: Success
- 1: Task not found or validation error

---

## Command: update

**Syntax**: `uv run main.py update <id> "<description>"`

**Input**:
- `id` (integer, required): Task ID to update
- `description` (string, required): New task description

**Output (Success)**:
```
✅ Task updated successfully!
Before: Buy milk
After:  Buy almond milk
┌─────┬──────────────────┬────────┐
│ ID  │ Description      │ Status │
├─────┼──────────────────┼────────┤
│ 1   │ Buy almond milk  │ ☐      │
└─────┴──────────────────┴────────┘
```

**Output (Error - Not Found)**:
```
❌ Error: Task with ID 99 not found.
Use 'uv run main.py list' to see all tasks.
```

**Output (Error - Invalid ID)**:
```
❌ Error: ID must be a positive integer.
Usage: uv run main.py update <id> "<description>"
```

**Output (Error - Empty Description)**:
```
❌ Error: Description cannot be empty.
Usage: uv run main.py update <id> "<description>"
```

**Behavior**:
1. Validate ID is positive integer
2. Validate description is non-empty
3. Find task by ID
4. Update description (preserve completed status)
5. Save to tasks.json
6. Display before/after confirmation

**Exit Codes**:
- 0: Success
- 1: Task not found or validation error

---

## Command: delete

**Syntax**: `uv run main.py delete <id>`

**Input**:
- `id` (integer, required): Task ID to delete

**Output (Success)**:
```
✅ Task deleted successfully!
Removed: [1] Buy groceries
```

**Output (Error - Not Found)**:
```
❌ Error: Task with ID 99 not found.
Use 'uv run main.py list' to see all tasks.
```

**Output (Error - Invalid ID)**:
```
❌ Error: ID must be a positive integer.
Usage: uv run main.py delete <id>
```

**Behavior**:
1. Validate ID is positive integer
2. Find task by ID
3. Remove task from list
4. Save to tasks.json
5. Display confirmation with deleted task details

**Exit Codes**:
- 0: Success
- 1: Task not found or validation error

---

## Command: (none/help)

**Syntax**: `uv run main.py` or `uv run main.py --help`

**Output**:
```
📋 Todo CLI - Manage your tasks from the command line

Commands:
  add "<description>"      Add a new task
  list                     Show all tasks
  complete <id>            Toggle task completion
  update <id> "<desc>"     Update task description
  delete <id>              Remove a task

Examples:
  uv run main.py add "Buy groceries"
  uv run main.py list
  uv run main.py complete 1
  uv run main.py update 1 "Buy organic groceries"
  uv run main.py delete 1
```

**Exit Codes**:
- 0: Success

---

## Command: (invalid)

**Syntax**: `uv run main.py <unknown_command>`

**Output**:
```
❌ Error: Unknown command '<unknown_command>'

📋 Todo CLI - Manage your tasks from the command line

Commands:
  add "<description>"      Add a new task
  list                     Show all tasks
  complete <id>            Toggle task completion
  update <id> "<desc>"     Update task description
  delete <id>              Remove a task
```

**Exit Codes**:
- 1: Error

---

## UI Formatting Standards

### Colors
- Success: Green (✅)
- Error: Red (❌)
- Info/Header: Blue (📋)
- Completed task: Green text or strikethrough
- Pending task: Default text

### Icons
- Completed: ☑ or ✓
- Pending: ☐ or ○
- Success: ✅
- Error: ❌
- List header: 📋

### Table Style
- Borders: Box drawing characters
- Header row: Bold
- Columns: ID (right-aligned), Description (left-aligned), Status (centered)
