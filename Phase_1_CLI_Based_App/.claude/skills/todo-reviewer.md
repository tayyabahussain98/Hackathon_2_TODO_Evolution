# Skill: todo-reviewer

Review implementation for correctness and alignment.

## Purpose

- Catch mistakes before merging
- Ensure implementation matches task requirements
- Maintain quality and consistency across codebase

## When to Use

- After builder completes a task
- Before marking a task as done
- During code review phase of workflow

## Inputs

- Implemented code (files modified/created)
- Task description from `specs/<feature-name>/tasks.md`
- Reference to plan and spec for context

## Outputs

- Approval (APPROVED) or requested fixes (CHANGES REQUESTED)
- List of issues if any
- Recommendations for improvement

## Procedure

1. **Compare Code to Task Requirements**
   - Read the task description carefully
   - Check each expected output is implemented
   - Verify only specified files were modified
   - Confirm no scope creep occurred
   - Example:
     ```
     Task T-101 Expected:
     ✓ TodoItem dataclass created
     ✓ Has id, title, completed, created_at
     ✓ to_dict() method implemented
     ✗ from_dict() method missing  ← Issue found
     ```

2. **Validate Acceptance Criteria**
   - Cross-reference with spec acceptance criteria
   - Verify each criterion is satisfied
   - Check edge cases are handled
   - Example:
     ```
     Acceptance Criteria Check:
     ✓ AC-1: User can create todo item
     ✓ AC-2: Empty title rejected
     ✓ AC-3: ID auto-generated if not provided
     ```

3. **Check Tests**
   - Verify all test checklist items have tests
   - Run tests and confirm they pass
   - Check test quality (meaningful assertions)
   - Verify edge cases are covered
   - Example:
     ```
     Test Checklist Review:
     ✓ test_create_todo_item_valid - exists, passes
     ✓ test_empty_title_raises_error - exists, passes
     ✗ test_to_dict_format - missing test
     ```

4. **Recommend Improvements**
   - Note code quality issues (not blockers)
   - Suggest better patterns if applicable
   - Flag potential bugs or edge cases
   - Keep recommendations minimal and actionable
   - Example:
     ```
     Recommendations (non-blocking):
     - Consider adding __repr__ for debugging
     - Type hint on line 15 could be more specific
     ```

5. **Render Verdict**
   - APPROVED: All requirements met, tests pass
   - CHANGES REQUESTED: Issues must be fixed
   - Provide clear, actionable feedback

## Quality Checklist

- [ ] Nothing outside scope implemented (no extras)
- [ ] Structure follows plan architecture
- [ ] Code is readable and maintainable
- [ ] All expected outputs present
- [ ] All tests exist and pass
- [ ] No hardcoded values that should be configurable
- [ ] Error handling matches plan strategy
- [ ] No security issues (injection, secrets, etc.)

## Avoid

- **Changing requirements**: Review against what was specified
- **Approving incomplete work**: All checklist items must pass
- **Nitpicking style**: Focus on correctness, not preferences
- **Suggesting new features**: Out of scope for review
- **Being vague**: Provide specific, actionable feedback
- **Blocking on non-issues**: Distinguish blockers from suggestions

## Review Verdict Criteria

### APPROVED
- All task requirements implemented
- All tests defined in checklist exist and pass
- No scope creep (nothing extra added)
- Code follows plan architecture
- No critical issues found

### CHANGES REQUESTED
- Missing required functionality
- Tests missing or failing
- Scope creep detected
- Architecture deviation from plan
- Security or correctness issues

## Example Review Output

```markdown
# Review: T-101 - Create TodoItem dataclass

## Summary
**Verdict:** CHANGES REQUESTED

## Requirements Check

| Requirement | Status | Notes |
|-------------|--------|-------|
| TodoItem dataclass | ✓ PASS | Correctly implemented |
| id attribute | ✓ PASS | str type as specified |
| title attribute | ✓ PASS | str type as specified |
| completed attribute | ✓ PASS | bool, defaults to False |
| created_at attribute | ✓ PASS | datetime with default |
| to_dict() method | ✓ PASS | Returns correct format |
| from_dict() method | ✗ FAIL | Not implemented |

## Acceptance Criteria

| Criteria | Status |
|----------|--------|
| AC-1: Create todo | ✓ PASS |
| AC-2: Empty title rejected | ✓ PASS |

## Test Review

| Test | Status |
|------|--------|
| test_create_valid | ✓ EXISTS, PASSES |
| test_empty_title | ✓ EXISTS, PASSES |
| test_to_dict | ✓ EXISTS, PASSES |
| test_from_dict | ✗ MISSING |

## Issues (Must Fix)

1. **Missing from_dict() method**
   - Location: src/models.py
   - Task requires: "from_dict() class method for deserialization"
   - Action: Implement from_dict() classmethod

2. **Missing test for from_dict()**
   - Location: tests/test_models.py
   - Task requires: "Test from_dict() reconstructs object correctly"
   - Action: Add test_from_dict_reconstructs_object()

## Recommendations (Optional)

1. Consider adding `__eq__` method for easier testing
2. Line 23: Type hint could use `Optional[str]` for clarity

## Next Steps

1. Implement from_dict() classmethod
2. Add missing test
3. Re-submit for review
```

## Review Workflow

```
Builder completes task
        ↓
Reviewer receives code + task
        ↓
    Run review procedure
        ↓
   ┌────┴────┐
   │         │
APPROVED   CHANGES REQUESTED
   │         │
   ↓         ↓
Mark task  Return to builder
complete   with feedback
```

## Related Skills

- `todo-builder` - Produces code for review
- `todo-tasks` - Source of task requirements
- `todo-planning` - Reference for architecture
- `todo-specification` - Reference for acceptance criteria
