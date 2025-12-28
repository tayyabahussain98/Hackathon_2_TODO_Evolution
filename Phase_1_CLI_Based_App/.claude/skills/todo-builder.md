# Skill: todo-builder

Implement one task at a time in Python.

## Purpose

- Generate safe, modular code based on task definitions
- Ensure incremental, testable progress
- Maintain code quality without scope creep

## When to Use

- When a task is approved and ready for implementation
- During the implementation phase of the workflow
- When moving from T-00X to T-00Y in the task list

## Inputs

- Task description from `specs/<feature-name>/tasks.md`
- Specific task ID (e.g., T-101)
- Reference to plan and spec if clarification needed

## Outputs

- Python code implementing the task
- Tests as defined in task checklist
- Updated task status (mark complete when done)

## Procedure

1. **Read Task Carefully**
   - Understand the task description fully
   - Review expected output
   - Check dependencies are complete
   - Identify files to create/modify
   - Review test checklist
   - Example:
     ```
     Task T-101: Create TodoItem dataclass
     Files: CREATE src/models.py
     Expected: TodoItem with id, title, completed, created_at
     Tests: 4 test cases defined
     ```

2. **Modify Only Specified Files**
   - Work only on files listed in the task
   - If a file doesn't exist, create it
   - If modifying, read existing code first
   - Never touch files outside task scope
   - Example:
     ```
     Task says: CREATE src/models.py
     Action: Create src/models.py only
     Do NOT touch: cli.py, storage.py, etc.
     ```

3. **Implement Minimum Code to Pass Task**
   - Write only what's needed to meet expected output
   - No "while I'm here" improvements
   - No anticipating future tasks
   - Keep functions small and focused
   - Example:
     ```python
     # Task: Create TodoItem dataclass
     # Do this:
     @dataclass
     class TodoItem:
         id: str
         title: str
         completed: bool = False
         created_at: datetime = field(default_factory=datetime.now)

     # Do NOT add:
     # - Extra methods not in task
     # - Validation not specified
     # - Logging, caching, etc.
     ```

4. **Add Basic Tests if Defined**
   - Implement tests from the task's test checklist
   - One test per checklist item
   - Use pytest conventions
   - Test the task's scope only
   - Example:
     ```python
     # Test Checklist:
     # - [ ] Create TodoItem with valid data
     # - [ ] Validate empty title raises ValueError

     def test_create_todo_item_valid():
         item = TodoItem(id="1", title="Test")
         assert item.title == "Test"

     def test_empty_title_raises_error():
         with pytest.raises(ValueError):
             TodoItem(id="1", title="")
     ```

5. **Verify and Report**
   - Run the tests for this task
   - Confirm expected output is achieved
   - Report completion status
   - Note any blockers or questions

## Quality Checklist

- [ ] No extra features beyond task scope
- [ ] No architecture changes unless specified
- [ ] Code is readable and simple
- [ ] Only specified files modified
- [ ] All task tests pass
- [ ] No hardcoded values that should be configurable
- [ ] Follows Python conventions (PEP 8)
- [ ] No unused imports or dead code

## Avoid

- **Guessing requirements**: If unclear, ask or check spec/plan
- **Editing unrelated files**: Stay within task boundaries
- **Over-engineering**: No abstractions for single use
- **Future-proofing**: Implement for now, not "just in case"
- **Refactoring**: Don't improve existing code unless task says so
- **Adding comments for obvious code**: Self-documenting code preferred
- **Changing function signatures**: Unless task explicitly requires it

## Implementation Patterns

### Creating a New File
```python
# 1. Add module docstring
"""Module description matching file responsibility from plan."""

# 2. Imports (stdlib → third-party → local)
from dataclasses import dataclass
from datetime import datetime

# 3. Implementation (minimal, task-scoped)
@dataclass
class TodoItem:
    ...
```

### Modifying an Existing File
```python
# 1. Read the file first
# 2. Identify exact location for changes
# 3. Make minimal modification
# 4. Preserve existing code style
```

### Writing Tests
```python
# 1. One test file per source file
# 2. Test function names describe behavior
# 3. Arrange-Act-Assert pattern
# 4. Cover checklist items only

def test_<behavior_being_tested>():
    # Arrange
    item = TodoItem(id="1", title="Test")

    # Act
    result = item.to_dict()

    # Assert
    assert result["title"] == "Test"
```

## Example Task Execution

```markdown
## Executing T-101: Create TodoItem dataclass

**Reading task...**
- Description: Create TodoItem data structure
- Files: CREATE src/models.py, CREATE tests/test_models.py
- Expected: dataclass with id, title, completed, created_at
- Tests: 4 items

**Implementation:**
Created src/models.py with TodoItem dataclass
Created tests/test_models.py with 4 tests

**Verification:**
$ pytest tests/test_models.py -v
4 passed

**Status:** T-101 COMPLETE
```

## Related Skills

- `todo-tasks` - Provides task definitions
- `todo-planning` - Reference for design decisions
- `todo-specification` - Reference for requirements
