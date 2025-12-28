<!--
SYNC IMPACT REPORT
==================
Version change: N/A (new) -> 1.0.0
Modified principles: N/A (initial creation)
Added sections:
  - Core Principles (6 principles)
  - Architecture section
  - Process & Roles section
  - Governance section
Removed sections: N/A
Templates requiring updates:
  - .specify/templates/plan-template.md: ✅ Compatible (Constitution Check section will use these principles)
  - .specify/templates/spec-template.md: ✅ Compatible (scope aligns with Features Only principle)
  - .specify/templates/tasks-template.md: ✅ Compatible (task phases align with pipeline)
Follow-up TODOs: None
-->

# Python CLI Todo App Constitution

## Core Principles

### I. AI-Only Development

All code in this project MUST be AI-generated. No manual coding is permitted.

**Rationale**: Ensures consistency in code generation approach and validates AI-driven development workflows. Human intervention is limited to specification, review, and approval.

### II. Strict Pipeline

Development MUST follow the pipeline: **Specify → Plan → Tasks → Implement → Review**

- No shortcuts or skipping phases
- No guessing or assumptions without specification approval
- No architecture changes outside the planning phase
- Each phase MUST complete before the next begins

**Rationale**: Enforces disciplined, traceable development where every implementation decision traces back to approved specifications.

### III. Technology Stack

The following technology constraints are NON-NEGOTIABLE:

- **Python**: Version 3.11 or higher
- **Interface**: CLI only (command-line interface)
- **Storage**: File-based JSON storage (tasks.json)
- **Package Manager**: UV (uv) exclusively
- **UI Library**: rich for CLI formatting (tables, colors, icons)
- **Dependencies**: Minimal - standard library plus rich only

**Prohibited**:
- No external databases
- No web frameworks
- No GUI frameworks

**Rationale**: Keeps the project focused, portable, and simple while delivering a polished CLI experience.

### IV. UV Package Management

All project and dependency management MUST use UV:

```bash
uv init .              # Initialize in current directory
uv venv                # Create virtual environment
source .venv/bin/activate  # Activate (or Windows equivalent)
uv add <package>       # Add dependencies
```

**Prohibited**:
- pip
- poetry
- conda
- Manual venv creation

**Rationale**: UV provides fast, reproducible dependency management. Standardizing on one tool eliminates environment inconsistencies.

### V. Essential Features Only

The application MUST implement exactly these features:

| Feature | Command | Description |
|---------|---------|-------------|
| Add Task | `uv run main.py add "description"` | Create new task |
| Delete Task | `uv run main.py delete <id>` | Remove task by ID |
| Update Task | `uv run main.py update <id> "new description"` | Edit task description |
| View Tasks | `uv run main.py list` | Show all tasks with status |
| Complete Task | `uv run main.py complete <id>` | Toggle completed status |

**Task Properties** (exactly these, no more):
- ID (integer, auto-assigned)
- Description (string)
- Completed (boolean)

**Explicitly Out of Scope**:
- Due dates
- Priorities
- Categories/tags
- Sorting options
- Search/filter
- GUI/web interface
- Authentication
- Multi-user support

**Rationale**: Scope discipline prevents feature creep and keeps the MVP focused on core functionality with excellent UX.

### VI. Code Quality

All code MUST adhere to these standards:

- **Type hints**: All function signatures MUST include type annotations
- **Docstrings**: All public functions and classes MUST have docstrings
- **PEP 8**: Code MUST follow PEP 8 style guidelines
- **Separation of concerns**: Each module has a single responsibility
- **No globals**: State MUST be passed explicitly, not stored in global variables
- **Rich UI**: All CLI output MUST use rich formatting (tables, colors, icons)

**Rationale**: Maintains code readability, maintainability, and professional quality.

## Architecture

The project structure is FIXED and MUST NOT be altered:

```
.                           # Project root (current directory)
├── pyproject.toml          # Managed by uv
├── main.py                 # CLI entry point
├── tasks.json              # JSON storage (auto-generated)
└── src/                    # All source modules
    ├── models.py           # Task dataclass
    ├── services.py         # Business logic (CRUD operations)
    ├── storage.py          # JSON persistence (load/save)
    └── ui.py               # Rich-based UI formatting
```

**Module Responsibilities**:

- **main.py**: Command parsing, orchestration, entry point. Imports from src/.
- **src/models.py**: Task dataclass definition with ID, description, completed fields.
- **src/services.py**: Add, delete, update, complete, list operations. Pure logic, no I/O.
- **src/storage.py**: Load tasks from JSON, save tasks to JSON. File I/O only.
- **src/ui.py**: Rich console output, table formatting, icons, colors, prompts.

**Rationale**: Clear separation enables independent testing, reduces coupling, and makes the codebase navigable.

## Process & Roles

### Builder Role

The Builder (AI agent implementing code):
- MUST only implement tasks with approved task IDs
- MUST NOT add features beyond the task specification
- MUST include rich UI formatting in all implementations
- MUST NOT modify architecture or add new files

### Reviewer Role

The Reviewer (AI agent or human reviewing code):
- MUST verify strict match to spec and task requirements
- MUST verify UI formatting meets rich library standards (tables, icons, colors)
- MUST reject any scope creep or unauthorized additions
- MUST verify code quality standards (type hints, docstrings, PEP 8)

### Approval Flow

1. Specification approved before planning
2. Plan approved before task generation
3. Tasks approved before implementation
4. Implementation reviewed before merge

## Governance

This constitution is **final and binding** for the Python CLI Todo App project.

### Amendment Process

1. Proposed changes MUST be documented with rationale
2. Changes MUST be reviewed and approved before implementation
3. Version MUST be incremented according to semantic versioning:
   - **MAJOR**: Backward-incompatible principle changes or removals
   - **MINOR**: New principles or sections added
   - **PATCH**: Clarifications, wording fixes, non-semantic changes
4. Amendment date MUST be updated

### Compliance

- All PRs and code reviews MUST verify constitutional compliance
- Constitutional violations block merge
- Complexity beyond constitution MUST be justified in writing

**Version**: 1.0.0 | **Ratified**: 2025-12-27 | **Last Amended**: 2025-12-27
