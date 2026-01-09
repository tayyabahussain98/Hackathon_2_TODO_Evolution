<!--
SYNC IMPACT REPORT
==================
Version Change: [TEMPLATE] → 1.0.0
Type: INITIAL CONSTITUTION (Full-Stack Todo System)

Principles Added:
  I. Spec-Driven Workflow (NON-NEGOTIABLE)
  II. Layer Separation
  III. Backend Architecture
  IV. Frontend Architecture
  V. Authentication Architecture
  VI. Database Architecture
  VII. Monorepo Structure
  VIII. Task Definition Standard

Sections Added:
  - Implementation Standards
  - Review Standards
  - Governance

Templates Status:
  ⚠️ .specify/templates/plan-template.md - Needs review for layer separation checks
  ⚠️ .specify/templates/spec-template.md - Needs review for workflow alignment
  ⚠️ .specify/templates/tasks-template.md - Needs update for task definition standards
  ⚠️ .specify/templates/commands/*.md - Needs review for principle references

Follow-up TODOs:
  - Review and update all template files for consistency with new principles
  - Ensure agent definitions align with layer separation rules
  - Validate skill definitions match architectural boundaries
-->

# Full-Stack Todo System Constitution

## Core Principles

### I. Spec-Driven Workflow (NON-NEGOTIABLE)

**All development MUST follow: Specify → Plan → Tasks → Implement → Review**

- NO coding before specification exists
- NO skipping the planning phase
- NO implementation without task breakdown
- NO shortcuts or "temporary hacks" that bypass workflow

**Rationale**: Maintains architectural integrity, prevents technical debt, ensures all code
serves documented requirements, and enables effective code review against specifications.

### II. Layer Separation

**Strict separation of concerns across all architectural layers. NO mixing of responsibilities.**

**Backend Layer**:
- Routes: API endpoints only (HTTP concerns)
- Services: Business logic only
- Models: Data contracts only
- Middleware: Authentication and security only
- ❌ NEVER: UI code in backend
- ❌ NEVER: SQL queries in route handlers

**Frontend Layer**:
- Components: Reusable UI elements only
- Pages: Layout and composition only
- lib/api: All backend communication centralized
- ❌ NEVER: Direct database access from frontend
- ❌ NEVER: Business logic inside components

**Authentication Layer**:
- JWT sessions for stateless authentication
- Google OAuth support (planned architecture)
- Secrets MUST be environment variables, NEVER hardcoded
- Reusable across applications

**Database Layer**:
- Schema definitions controlled via migrations
- All changes tracked and versioned
- ❌ NEVER: Manual database modifications

**Rationale**: Clear boundaries enable independent testing, simplify debugging, allow parallel
development, facilitate reuse, and prevent cascading changes across layers.

### III. Backend Architecture

**Backend MUST adhere to clean architecture with strict layer responsibilities.**

**Structure**:
```
backend/app/
├── main.py          # Application entry point
├── routes/          # API endpoints (thin controllers)
├── services/        # Business logic
├── models/          # Data contracts (Pydantic/SQLModel)
├── middleware/      # Auth, logging, error handling
└── core/            # Configuration, dependencies
```

**Rules**:
- Routes handle HTTP only: request parsing, response formatting, status codes
- Services contain ALL business logic: validation, transformations, orchestration
- Models define data shape: request/response schemas, database tables
- Middleware handles cross-cutting concerns: JWT verification, CORS, logging
- Database queries MUST exist in services or repository layer, NEVER in routes

**Rationale**: Thin controllers keep routes testable, business logic reusable, and enable
easy migration to different frameworks or protocols.

### IV. Frontend Architecture

**Frontend MUST be component-based with centralized API communication.**

**Structure**:
```
frontend/
├── app/             # Next.js pages (App Router)
├── components/      # Reusable UI components
├── lib/
│   └── api.ts      # Centralized API client (ONLY place for backend calls)
└── auth-ui/        # Authentication UI components
```

**Rules**:
- Components MUST be reusable and single-purpose
- ALL backend communication goes through lib/api.ts
- NO fetch() or axios calls outside lib/api.ts
- NO business logic in components (delegate to backend)
- NO direct database access from frontend code

**Rationale**: Centralized API layer enables token management, error handling, request
interceptors, and prevents scattered backend logic across components.

### V. Authentication Architecture

**Authentication MUST be secure, reusable, and prepared for OAuth integration.**

**Structure**:
```
auth/
├── config/         # Better Auth configuration
├── tokens/         # JWT generation, validation
├── providers/      # OAuth providers (Google planned)
└── docs/           # Authentication documentation
```

**Rules**:
- JWT tokens for stateless session management
- Better Auth integration for unified auth flow
- Google OAuth architecture planned (not yet implemented)
- Secrets stored in environment variables (BETTER_AUTH_SECRET, JWT_SECRET)
- ❌ NEVER: Hardcode secrets, tokens, or credentials
- ❌ NEVER: Store passwords in plaintext

**Rationale**: Reusable auth layer enables multi-app deployment, OAuth integration, and
centralized security management.

### VI. Database Architecture

**Database schema MUST be version-controlled and migration-driven.**

**Structure**:
```
database/
├── schema/         # SQLModel table definitions
├── migrations/     # Alembic migrations (tracked)
└── seeds/          # Development/test data
```

**Rules**:
- ALL schema changes via migrations (no manual ALTER TABLE)
- Migrations MUST be reversible (up + down functions)
- Schema defined using SQLModel
- Foreign keys and indexes explicitly defined
- ❌ NEVER: Modify database schema manually
- ❌ NEVER: Skip migration creation for schema changes

**Rationale**: Migration-driven development ensures reproducible environments, enables
rollback, documents schema evolution, and prevents environment drift.

### VII. Monorepo Structure

**Project MUST follow standardized monorepo organization with domain separation.**

**Top-Level Structure**:
```
project/
├── specs/          # Feature specifications (Specify phase)
├── agents/         # Domain-specific agents and skills
│   ├── backend/
│   ├── frontend/
│   ├── auth/
│   └── database/
├── backend/        # Backend application code
├── frontend/       # Frontend application code
├── auth/           # Authentication services
├── database/       # Schema and migrations
└── shared/         # Cross-layer utilities and types
```

**Rules**:
- Each domain has dedicated folder structure
- Agents live in .claude/agents/{domain}/ with their skills/
- Code lives in {domain}/ (backend/, frontend/, auth/, database/)
- Shared utilities only for truly cross-layer code
- ❌ NEVER: Mix code from different layers in the same file
- ❌ NEVER: Place implementation code in agent folders

**Rationale**: Clear structure enables domain experts to work independently, simplifies
navigation, enforces separation of concerns, and scales to large teams.

### VIII. Task Definition Standard

**Every task MUST be fully specified before implementation begins.**

**Required Task Elements**:
- **Task ID**: Unique identifier for tracking
- **Purpose**: Clear statement of what and why
- **Files Involved**: Explicit list of files to create/modify
- **Acceptance Criteria**: Testable conditions for completion
- **Out-of-Scope**: Explicit boundaries of what task does NOT include
- **Validation Checklist**: Steps to verify correctness

**Rules**:
- NO task = NO code (absolute requirement)
- Tasks MUST be granular (2-4 hours maximum)
- Tasks MUST reference spec section they implement
- Tasks MUST be ordered by dependencies
- ❌ NEVER: Start implementation without approved task definition
- ❌ NEVER: Expand task scope during implementation (create new task instead)

**Rationale**: Precise task definition enables accurate estimation, parallel work, clear
acceptance testing, and prevents scope creep.

## Implementation Standards

**Code implementation MUST adhere to these quality and boundary rules.**

**General Rules**:
- Implement ONLY the assigned task (no scope expansion)
- Code MUST be readable and self-documenting
- Code MUST be testable (pure functions, dependency injection)
- Respect folder boundaries (no cross-layer imports except via shared/)
- Reuse existing helpers and utilities (no duplication)

**Testing Requirements**:
- Unit tests for business logic (services, utilities)
- Integration tests for API endpoints
- Component tests for UI elements
- Tests MUST be written before implementation (TDD preferred)

**Documentation Requirements**:
- Docstrings for public functions and classes
- Inline comments for complex logic only
- API endpoint documentation (request/response schemas)
- README updates for new features or setup changes

## Review Standards

**Code review MUST verify compliance with constitution and specifications.**

**Approval Criteria** (ALL must be met):
- ✅ Matches specification exactly
- ✅ Follows architecture rules (layer separation)
- ✅ Code exists in correct folder for its domain
- ✅ Adds nothing beyond task requirements
- ✅ Code is readable and maintainable
- ✅ Tests exist and pass
- ✅ No hardcoded secrets or configuration

**Rejection Triggers** (ANY triggers rejection):
- ❌ Violates layer separation (e.g., SQL in routes)
- ❌ Mixes concerns (e.g., business logic in components)
- ❌ Code in wrong folder (e.g., frontend code in backend/)
- ❌ Scope creep (implements beyond task definition)
- ❌ Hardcoded secrets or credentials
- ❌ Missing tests for new functionality
- ❌ Bypasses workflow (no spec/plan/task)

**Review Process**:
1. Verify task exists and is approved
2. Check code location matches task files list
3. Validate layer boundaries not violated
4. Confirm no scope expansion occurred
5. Review tests exist and cover requirements
6. Verify no hardcoded configuration
7. Approve or request fixes with specific references

## Governance

**This constitution is the supreme authority for all development practices.**

**Amendment Process**:
- Amendments MUST be proposed with rationale
- Amendments MUST be discussed and approved
- Version bumped following semantic versioning (MAJOR.MINOR.PATCH)
- All dependent templates and docs MUST be updated
- Migration plan required for breaking changes

**Versioning Policy**:
- MAJOR: Backward-incompatible principle changes or removals
- MINOR: New principles added or material expansions
- PATCH: Clarifications, wording improvements, typo fixes

**Compliance Review**:
- ALL pull requests MUST verify constitution compliance
- Violations MUST be documented and corrected
- Repeated violations trigger architecture review
- Constitution takes precedence over convenience

**Enforcement**:
- Code reviews MUST check constitution compliance
- CI/CD gates verify folder structure and layer boundaries
- Architecture decisions MUST reference constitution principles
- Team leads responsible for ensuring adherence

**Runtime Guidance**:
- Development guidance maintained in CLAUDE.md
- Agent instructions reference constitution principles
- Skills implement constitution-compliant patterns

**Version**: 1.0.0 | **Ratified**: 2025-12-28 | **Last Amended**: 2025-12-28
