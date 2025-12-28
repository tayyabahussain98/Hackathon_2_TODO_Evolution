---
id: 001
title: Python CLI Todo Constitution Init
stage: constitution
date: 2025-12-27
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: system
command: /sp.constitution
labels: ["constitution", "init", "todo-app", "python-cli"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (constitution document, no tests)
---

## Prompt

## Python CLI Todo App – Core Constitution

### 1. Core Rules
- No manual coding. Only AI-generated.
- Strict pipeline: **Specify → Plan → Tasks → Implement → Review**
- No shortcuts, no guessing, no architecture changes.

### 2. Technology
- Python 3.11+
- CLI only (command-line interface)
- File-based storage (JSON)
- **UV package manager must be used** for project setup and dependency management
- Dependencies: Minimal (standard library + rich for CLI UI formatting; uv add rich if needed)
- No external databases or web frameworks

### 3. Project Initialization Rules
- Project **must** be initialized with **uv** in the **current directory** (no new folder creation):
uv init .
uv venv
source .venv/bin/activate  # or equiv on Windows
text- Use **uv add** for any dependencies (e.g., `uv add rich` for CLI UI)
- **pyproject.toml** must be created and managed via uv in the root
- Virtual environment must be created and used via uv
- No pip, poetry, or manual venv allowed

### 4. Core Essential Features (Exact Scope)
Must implement **only** these, with rich CLI UI formatting:

| Feature              | Command Example          | Description                          | UI Formatting |
|----------------------|--------------------------|--------------------------------------|---------------|
| Add Task             | `uv run main.py add "Buy milk"` | Add new task | Prompt with icons (e.g., ✅ Added) and formatted confirmation |
| Delete Task          | `uv run main.py delete 2` | Remove task by ID | Warning prompt, table update with strikethrough or icons |
| Update Task          | `uv run main.py update 2 "Buy bread"` | Edit task description | Interactive prompt for edit, show before/after in table |
| View Task List       | `uv run main.py list`    | Show all tasks with ID & status | Formatted table (using rich) with columns: ID, Description, Status ([x] or [ ]), borders, colors |
| Mark as Complete     | `uv run main.py complete 2` | Toggle completed status | Icon-based toggle (e.g., [ ] → [x]), refresh table view |

- Tasks: ID, description, completed (bool)
- Persistence: Auto-save/load from JSON file (e.g., tasks.json in root)
- CLI UI: Use **rich library** for website-like feel – tables, colors, icons (e.g., ✅, ❌, spinner for loading), borders, progress indicators. Make it interactive and visually appealing like a terminal "website" (e.g., clear screen, menus, styled outputs).

### 5. Out of Scope
No due dates, priorities, categories, sorting, GUI, web, auth, etc.

### 6. Architecture (Root = Current Directory)
.                        # Project root (current directory)
├── pyproject.toml       # Managed by uv
├── main.py              # CLI entry point (main executable script, handles commands)
├── tasks.json           # JSON storage file (auto-generated)
└── src/                 # All other Python files in this folder
├── models.py        # Task dataclass
├── services.py      # Logic (add, delete, update, complete, list)
├── storage.py       # JSON load/save
└── ui.py            # Rich-based UI formatting (tables, icons, prompts)
text- main.py in root: Parses commands, calls src/ modules, handles UI output.
- src/ folder: Modular code separation.

### 7. Quality
- Type hints
- Docstrings
- PEP 8
- Separation of concerns
- No globals
- Rich UI: Every output formatted (e.g., tables with colors/icons, prompts with styling) to feel "website-like" in CLI.

### 8. Process
- Code only from approved tasks (with ID)
- Builder: no extras, include rich UI in implementations
- Reviewer: strict match to spec/tasks, verify UI formatting (tables/icons)

This constitution is final and binding.

## Response snapshot

Created Python CLI Todo App Constitution v1.0.0 with:
- 6 Core Principles: AI-Only Development, Strict Pipeline, Technology Stack, UV Package Management, Essential Features Only, Code Quality
- Architecture section with fixed project structure
- Process & Roles section defining Builder and Reviewer responsibilities
- Governance section with amendment process and compliance requirements

All template placeholders replaced with concrete, testable values from user input.

## Outcome

- Impact: Established foundational governance document for Python CLI Todo App project
- Tests: N/A (constitution document)
- Files: .specify/memory/constitution.md (created/updated)
- Next prompts: /sp.specify to create feature specification
- Reflection: User provided comprehensive constitution input; mapped cleanly to 6 principles plus additional sections

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
