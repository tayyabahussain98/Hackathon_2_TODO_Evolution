# Skill: todo-tasks

Break plan into atomic, testable implementation tasks.

## Purpose

- Create clear roadmap for builder agent
- Enable incremental, verifiable progress
- Ensure nothing from the plan is missed

## When to Use

- After implementation plan is finalized and approved
- Before any code is written
- When transitioning from design to implementation phase

## Inputs

- Approved implementation plan (`specs/<feature-name>/plan.md`)
- Specification document for reference (`specs/<feature-name>/spec.md`)

## Outputs

- Ordered task list with dependencies
- Located at `specs/<feature-name>/tasks.md`

## Procedure

1. **Convert Each Step into a Task**
   - One task = one logical unit of work
   - Task should be completable in a single session
   - Clear start and end state
   - Example: "Create TodoItem model class" not "Build the model layer"

2. **Assign Task IDs**
   - Format: `T-001`, `T-002`, `T-003`...
   - Group by component: `T-1xx` for models, `T-2xx` for storage, etc.
   - Maintain sequential order within groups
   - Example:
     ```
     T-101: Create TodoItem dataclass
     T-102: Add validation to TodoItem
     T-201: Create storage interface
     T-202: Implement JSON file storage
     ```

3. **Define Files to Edit**
   - List exact file paths for each task
   - Specify if creating new file or modifying existing
   - Include test files
   - Example:
     ```
     Files:
     - CREATE: src/models.py
     - MODIFY: src/__init__.py
     - CREATE: tests/test_models.py
     ```

4. **Define Expected Output**
   - Describe what exists after task completion
   - Include observable behavior
   - Be specific and verifiable
   - Example:
     ```
     Expected Output:
     - TodoItem class with id, title, completed, created_at attributes
     - from_dict() and to_dict() methods work correctly
     - Validation raises ValueError for empty title
     ```

5. **Define Test Checklist**
   - List specific tests to write/pass
   - Include edge cases
   - Reference acceptance criteria from spec
   - Example:
     ```
     Test Checklist:
     - [ ] Test TodoItem creation with valid data
     - [ ] Test TodoItem creation with empty title raises error
     - [ ] Test to_dict() returns correct format
     - [ ] Test from_dict() reconstructs object correctly
     ```

## Quality Checklist

- [ ] Tasks are small (1-2 hours of work max)
- [ ] No ambiguity in task description
- [ ] Each task is independently testable
- [ ] Dependencies between tasks are explicit
- [ ] All plan components are covered
- [ ] No task combines multiple features
- [ ] File paths are specific and accurate
- [ ] Test criteria are concrete and verifiable

## Avoid

- **Combining multiple features**: One task = one feature unit
- **Vague descriptions**: "Improve storage" → "Add error handling to save_todo()"
- **Missing dependencies**: Always specify what must be done first
- **Untestable tasks**: If you can't test it, break it down further
- **Implementation details**: Describe WHAT, not HOW to code it
- **Large tasks**: If it takes more than 2 hours, split it

## Example Output Structure

```markdown
# Tasks: <feature-name>

## Overview
Total tasks: X
Estimated complexity: Low/Medium/High

## Task Groups

### Group 1: Models (T-1xx)

#### T-101: Create TodoItem dataclass
**Description:** Create the core TodoItem data structure.

**Dependencies:** None

**Files:**
- CREATE: `src/models.py`
- CREATE: `tests/test_models.py`

**Expected Output:**
- TodoItem dataclass with id, title, completed, created_at
- Serialization methods (to_dict, from_dict)

**Test Checklist:**
- [ ] Create TodoItem with valid data
- [ ] Validate empty title raises ValueError
- [ ] Verify to_dict output format
- [ ] Verify from_dict reconstruction

**Acceptance Criteria Reference:** US-001, F-001

---

#### T-102: Add TodoItem validation
...

### Group 2: Storage (T-2xx)
...

## Dependency Graph
```
T-101 → T-102 → T-201
              ↘ T-301
```

## Implementation Order
1. T-101 (no dependencies)
2. T-102 (requires T-101)
3. T-201 (requires T-102)
...
```

## Related Skills

- `todo-planning` - Must be completed before task breakdown
- `todo-specification` - Reference for acceptance criteria
