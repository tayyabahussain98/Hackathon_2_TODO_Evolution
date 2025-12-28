# Quickstart: CLI Todo Core Application

**Feature**: 001-cli-todo-core
**Date**: 2025-12-27

## Prerequisites

- Python 3.11 or higher
- UV package manager installed

## Setup

### 1. Initialize Project

```bash
# Navigate to project directory
cd /path/to/project

# Initialize with UV (in current directory)
uv init .

# Create virtual environment
uv venv

# Activate virtual environment
# Linux/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Install dependencies
uv add rich
```

### 2. Verify Installation

```bash
# Check Python version
python --version
# Expected: Python 3.11.x or higher

# Verify rich is installed
python -c "import rich; print(rich.__version__)"
# Expected: Version number (e.g., 13.x.x)
```

## Usage

### Add a Task

```bash
uv run main.py add "Buy groceries"
```

Output:
```
✅ Task added successfully!
┌─────┬─────────────────┬────────┐
│ ID  │ Description     │ Status │
├─────┼─────────────────┼────────┤
│ 1   │ Buy groceries   │ ☐      │
└─────┴─────────────────┴────────┘
```

### List All Tasks

```bash
uv run main.py list
```

Output:
```
📋 Your Tasks
┌─────┬─────────────────┬────────┐
│ ID  │ Description     │ Status │
├─────┼─────────────────┼────────┤
│ 1   │ Buy groceries   │ ☐      │
│ 2   │ Call dentist    │ ☑      │
└─────┴─────────────────┴────────┘
```

### Mark Task Complete

```bash
uv run main.py complete 1
```

Output:
```
✅ Task marked as complete!
┌─────┬─────────────────┬────────┐
│ ID  │ Description     │ Status │
├─────┼─────────────────┼────────┤
│ 1   │ Buy groceries   │ ☑      │
└─────┴─────────────────┴────────┘
```

### Update Task Description

```bash
uv run main.py update 1 "Buy organic groceries"
```

Output:
```
✅ Task updated successfully!
Before: Buy groceries
After:  Buy organic groceries
┌─────┬───────────────────────┬────────┐
│ ID  │ Description           │ Status │
├─────┼───────────────────────┼────────┤
│ 1   │ Buy organic groceries │ ☑      │
└─────┴───────────────────────┴────────┘
```

### Delete a Task

```bash
uv run main.py delete 1
```

Output:
```
✅ Task deleted successfully!
Removed: [1] Buy organic groceries
```

### Get Help

```bash
uv run main.py
```

Output:
```
📋 Todo CLI - Manage your tasks from the command line

Commands:
  add "<description>"      Add a new task
  list                     Show all tasks
  complete <id>            Toggle task completion
  update <id> "<desc>"     Update task description
  delete <id>              Remove a task
```

## Data Storage

Tasks are automatically saved to `tasks.json` in the project root directory.

```json
[
  {"id": 1, "description": "Buy groceries", "completed": false},
  {"id": 2, "description": "Call dentist", "completed": true}
]
```

## Validation Workflow

After implementation, verify all operations work correctly:

```bash
# 1. Start fresh
rm -f tasks.json

# 2. Add tasks
uv run main.py add "Task one"
uv run main.py add "Task two"
uv run main.py add "Task three"

# 3. List tasks
uv run main.py list

# 4. Complete a task
uv run main.py complete 2

# 5. Update a task
uv run main.py update 1 "Updated task one"

# 6. Delete a task
uv run main.py delete 3

# 7. Final list
uv run main.py list

# 8. Verify persistence
uv run main.py list  # Should show same tasks after restart
```

## Troubleshooting

### "Command not found" errors
- Ensure virtual environment is activated
- Ensure you're in the project root directory

### Import errors
- Run `uv add rich` to install the rich library
- Verify Python 3.11+ is being used

### File permission errors
- Ensure write permissions in project directory
- Check that tasks.json is not locked by another process
