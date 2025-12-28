# Skill: todo-planning

Convert specification into architecture and implementation plan.

## Purpose

- Translate WHAT (specification) into HOW (design)
- Create a clear blueprint for implementation without writing code

## When to Use

- After specification is approved
- When transitioning from requirements to design phase
- Before task breakdown begins

## Inputs

- Approved specification document (`specs/<feature-name>/spec.md`)
- Any architectural constraints from constitution

## Outputs

- Architecture and implementation plan
- Located at `specs/<feature-name>/plan.md`

## Procedure

1. **Define Folder Structure**
   - Map logical components to directories
   - Follow Python package conventions
   - Keep structure flat and intuitive
   - Example:
     ```
     todo_app/
     ├── __init__.py
     ├── cli.py
     ├── models.py
     ├── storage.py
     └── utils.py
     tests/
     └── ...
     ```

2. **Define File Responsibilities**
   - One clear purpose per file
   - Document what each file owns
   - Identify dependencies between files
   - Example:
     - `cli.py` - Command-line interface and argument parsing
     - `models.py` - Data structures and validation
     - `storage.py` - Persistence layer

3. **List Functions and Classes**
   - Name each function/class with purpose
   - Define inputs and outputs (types, not implementation)
   - Document public interface only
   - Example:
     ```
     class TodoItem:
         - id: str
         - title: str
         - completed: bool

     def add_todo(title: str) -> TodoItem
     def list_todos() -> List[TodoItem]
     ```

4. **Describe Data Flow**
   - Trace user action through system layers
   - Document state changes
   - Identify data transformations
   - Example:
     ```
     User Input → CLI Parser → Command Handler → Storage → Response → Output
     ```

5. **Identify Error Handling Strategies**
   - List expected error conditions
   - Define error response patterns
   - Document recovery strategies
   - Example:
     - File not found → Create new storage file
     - Invalid input → Return validation error message
     - Storage corruption → Backup and reset

## Quality Checklist

- [ ] Simple and modular design
- [ ] Matches specification requirements only (no extras)
- [ ] No code generation (signatures only)
- [ ] Each component has single responsibility
- [ ] Dependencies flow in one direction
- [ ] Error paths are documented
- [ ] Plan is implementable by following it step-by-step

## Avoid

- **Over-engineering**: No abstractions for single-use cases
- **Adding new features**: Only plan what's in the spec
- **Premature optimization**: Design for clarity first
- **Complex patterns**: No factories, adapters, or decorators unless truly needed
- **Writing actual code**: Signatures and descriptions only
- **Technology decisions not in spec**: Stick to stated constraints

## Example Output Structure

```markdown
# Implementation Plan: <feature-name>

## Architecture Overview
Brief description of the design approach.

## Folder Structure
```
project/
├── ...
```

## File Responsibilities

### <filename>
- **Purpose**: ...
- **Owns**: ...
- **Dependencies**: ...

## Component Design

### <component-name>
**Classes:**
- `ClassName` - purpose, attributes

**Functions:**
- `function_name(params) -> return` - purpose

## Data Flow

### <user-action>
1. Step 1...
2. Step 2...

## Error Handling

| Error Condition | Response | Recovery |
|-----------------|----------|----------|
| ... | ... | ... |

## Dependencies
- External: ...
- Internal: ...

## Open Design Questions
- ...
```

## Related Skills

- `todo-specification` - Must be completed before planning
- `todo-tasking` - Use after plan is approved
