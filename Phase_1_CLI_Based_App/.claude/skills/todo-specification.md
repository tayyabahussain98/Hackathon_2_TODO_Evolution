# Skill: todo-specification

Generate complete specification for Python CLI Todo App.

## Purpose

- Convert idea into clear requirements and user stories
- Define acceptance criteria and constraints

## When to Use

- When starting a new Todo CLI project
- When requirements are unclear or need formalization
- When you need a structured requirements document before planning

## Inputs

- Short description of the app or feature
- Any user-provided constraints or preferences

## Outputs

- Structured specification document in Markdown format
- Located at `specs/<feature-name>/spec.md`

## Procedure

1. **Identify Users**
   - Define primary user personas
   - Identify user goals and pain points
   - Document user context (CLI environment, technical level)

2. **Write User Stories**
   - Format: "As a [user], I want [action] so that [benefit]"
   - Cover all major user interactions
   - Include edge cases and error scenarios

3. **Define Features**
   - List core features with clear descriptions
   - Group related features logically
   - Prioritize features (must-have vs nice-to-have)

4. **Add Acceptance Criteria**
   - Each feature must have testable acceptance criteria
   - Use Given/When/Then format where appropriate
   - Include success and failure conditions

5. **Add Constraints and Out-of-Scope**
   - Technical constraints (Python version, dependencies)
   - Business constraints (timeline, resources)
   - Explicit out-of-scope items to prevent scope creep

## Quality Checklist

- [ ] No technical implementation details (no code, no architecture)
- [ ] All criteria are clear and testable
- [ ] No missing user flows
- [ ] All user stories have acceptance criteria
- [ ] Constraints are realistic and documented
- [ ] Out-of-scope items are explicitly listed
- [ ] Document follows consistent formatting

## Avoid

- Writing any code or pseudocode
- Choosing architecture or design patterns
- Making technology stack decisions beyond stated constraints
- Including implementation-specific details
- Assuming features not explicitly requested

## Example Output Structure

```markdown
# Feature Specification: <feature-name>

## Overview
Brief description of the feature.

## User Personas
- Primary: ...
- Secondary: ...

## User Stories
### US-001: <title>
As a [user], I want [action] so that [benefit].

**Acceptance Criteria:**
- [ ] Given..., When..., Then...

## Features
### F-001: <feature-name>
Description...

**Acceptance Criteria:**
- [ ] ...

## Constraints
- ...

## Out of Scope
- ...

## Open Questions
- ...
```

## Related Skills

- `todo-planning` - Use after specification is complete
- `todo-tasking` - Use after plan is approved
