# Implementation Plan: PostgreSQL Database Integration

**Feature Branch**: `003-postgres-storage`
**Created**: 2025-12-29
**Status**: Draft
**Based On**: spec.md
**Agent Leads**: database-agent (primary), schema-agent (models), migration-agent (Alembic)

## Executive Summary

This plan transitions the todo API from in-memory storage to persistent PostgreSQL storage using SQLAlchemy ORM and Alembic migrations. The implementation maintains full API compatibility with the existing frontend while adding data persistence capabilities.

**Key Change**: Replace in-memory list storage with SQLAlchemy async ORM backed by PostgreSQL.

---

## Scope and Dependencies

### In Scope
- Replace in-memory storage with PostgreSQL persistence using SQLAlchemy async ORM
- Create database engine, session management, and dependency injection
- Define SQLAlchemy Todo model with all required fields and constraints
- Configure Alembic for database migrations
- Update todo_service.py to use database sessions for all CRUD operations
- Generate and apply initial migration to create todos table
- Ensure data validation matches existing Pydantic model constraints

### Out of Scope
- User authentication or authorization
- Multi-tenancy or user-scoped data
- Additional data tables or relationships
- Advanced migration capabilities (data seeding, schema evolution beyond initial setup)
- Backup and restore functionality
- Database connection pooling configuration beyond defaults
- Real-time data synchronization

### External Dependencies
- PostgreSQL database (connection via environment configuration)
- SQLAlchemy 2.x with async support (already installed)
- AsyncPG driver (already installed)
- Alembic 1.x (already installed)
- Python-dotenv for configuration (already available via pydantic-settings)

---

## Architecture Decisions

### Decision 1: SQLAlchemy Async ORM
**Rationale**: SQLAlchemy 2.x with async support provides type-safe, database-agnostic ORM with excellent async support. Using asyncpg driver yields the best PostgreSQL performance for async FastAPI applications.

**Alternatives Considered**:
- Synchronous SQLAlchemy + sync driver - Would block FastAPI's async event loop
- Raw SQL queries - Would lose ORM benefits, increase boilerplate, reduce type safety
- Tortoise ORM - Less mature ecosystem than SQLAlchemy

**Trade-off**: Slight learning curve vs proven, widely-adopted solution with strong async support.

---

### Decision 2: Alembic for Migrations
**Rationale**: Alembic is the de facto standard migration tool for SQLAlchemy. Provides version control for schema, autogenerate support, and rollback capabilities.

**Alternatives Considered**:
- Manual SQL scripts - No version tracking, no autogenerate, manual rollback
- Alembic is already initialized in the project

**Trade-off**: Additional migration files vs robust schema evolution management.

---

### Decision 3: Separate Database Module (core/database.py)
**Rationale**: Centralizes database connection logic in a single module. Follows separation of concerns - routes handle HTTP, services handle business logic, core/database handles persistence layer.

**Alternatives Considered**:
- Database setup in main.py - Violates single responsibility, couples app lifecycle to persistence
- Database setup in each service - Duplicates connection logic, hard to maintain

**Trade-off**: Additional file vs clean separation and maintainability.

---

### Decision 4: Pydantic Models + SQLAlchemy Models Coexistence
**Rationale**: Pydantic models for request/response validation (already exist), SQLAlchemy models for database persistence. This separation allows different field types and validation rules for API vs database layers.

**Trade-off**: Duplicate model definitions vs flexibility and clarity between API contract and persistence schema.

---

## Interfaces and API Contracts

### Database Configuration
- **Source**: Environment variable (via pydantic-settings)
- **Variable**: `DATABASE_URL` (not .env file contents)
- **Format**: `postgresql+asyncpg://username:password@host:port/database`

### SQLAlchemy Model (Todo)
```python
Fields:
- id: Integer, primary_key=True, autoincrement=True
- description: String(500), nullable=False
- completed: Boolean, default=False
- created_at: DateTime, default=datetime.utcnow
- updated_at: DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
```

### Database Session Dependency
```python
def get_db():
    Dependency that yields AsyncSession
    Ensures session cleanup on request completion
```

### Service Layer Signatures (Updated)
- `create_todo(description: str, db: AsyncSession) -> TodoResponse`
- `list_todos(db: AsyncSession) -> List[TodoResponse]`
- `get_todo(todo_id: int, db: AsyncSession) -> TodoResponse`
- `update_todo(todo_id: int, description: Optional[str], completed: Optional[bool], db: AsyncSession) -> TodoResponse`
- `delete_todo(todo_id: int, db: AsyncSession) -> None`

**Change**: All service methods now require `db: AsyncSession` parameter for database operations.

---

## Non-Functional Requirements

### Performance
- **Read Operations**: Target < 2s for GET requests under normal load (100 concurrent users)
- **Write Operations**: Target < 2s for POST/PATCH/DELETE requests under normal load
- **Connection Pool**: SQLAlchemy's QueuePool default with pool_size=5, max_overflow=10
- **Database Index**: Consider index on `created_at` for future date-based queries

### Reliability
- **Connection Retries**: SQLAlchemy engine handles connection failures automatically
- **Transaction Rollback**: All database operations within transaction context
- **Session Cleanup**: Context manager ensures sessions are closed properly

### Security
- **No Password Logging**: Database URL never logged in production
- **Environment Configuration**: Connection details sourced from environment, not hardcoded
- **SQL Injection Protection**: SQLAlchemy ORM uses parameterized queries automatically

### Data Integrity
- **Column Constraints**: Database enforces NOT NULL on description
- **String Length**: Database enforces VARCHAR(500) limit on description
- **Timestamps**: Database defaults ensure created_at and updated_at are always set

---

## Data Management and Migration

### Source of Truth
- **Schema Definition**: SQLAlchemy model in `models/database_todo.py` (new file)
- **Migration Files**: `alembic/versions/*.py` - authoritative for production schema
- **Database**: PostgreSQL database is the actual data source of truth in production

### Schema Evolution
- Initial migration creates todos table with all required columns and constraints
- Future schema changes require new Alembic migrations
- Migration files must be reviewed before applying to production

### Migration and Rollback
- **Apply Migration**: `alembic upgrade head`
- **Rollback Migration**: `alembic downgrade -1` (or specific revision)
- **Migration Versioning**: Each migration has unique revision ID for tracking
- **Autogenerate**: Use `alembic revision --autogenerate -m "description"` for model changes

### Data Retention
- No automatic data purging
- All todos retained indefinitely (as per specification out-of-scope)
- Future: Consider soft delete pattern if audit trail becomes requirement

---

## Operational Readiness

### Observability
- **SQL Logging**: Configure SQLAlchemy logging for query inspection during development
- **Error Logging**: All database exceptions logged with context
- **Connection Pool Monitoring**: Engine events for connection open/close (optional, future enhancement)

### Alerting (Future)
- Connection pool exhaustion warnings
- Query execution time exceeding thresholds
- Database connection failures during startup

### Runbooks

#### Database Connection Failure on Startup
- **Symptom**: Application fails to start with database connection error
- **Diagnostic**: Check DATABASE_URL environment variable is set and valid
- **Action**: Verify PostgreSQL service is running, credentials are correct

#### Migration Failure
- **Symptom**: `alembic upgrade` fails with SQL error
- **Diagnostic**: Review migration SQL in `alembic/versions/` directory
- **Action**: Manually apply or rollback using PostgreSQL client

#### Query Performance Degradation
- **Symptom**: API responses exceed 2 second threshold
- **Diagnostic**: Enable SQLAlchemy logging, analyze slow queries
- **Action**: Add database indexes, optimize queries, or scale database

---

## Implementation Phases

### Phase 1: Database Infrastructure Setup

**Objective**: Create core database connection and session management.

**Tasks**:
1. Create `backend/core/database.py` with:
   - SQLAlchemy async engine configuration
   - AsyncSessionLocal factory
   - `get_db()` dependency injection function
   - Base declarative class export

**Files to Create**:
- `backend/core/database.py`

**Acceptance Criteria**:
- [ ] Database module imports without errors
- [ ] Engine can be instantiated using environment configuration
- [ ] `get_db()` dependency yields valid AsyncSession
- [ ] Session cleanup occurs automatically after request completion

**Manual Commands**: None

---

### Phase 2: SQLAlchemy Model Definition

**Objective**: Define the Todo SQLAlchemy model matching the specification.

**Tasks**:
1. Create `backend/models/database_todo.py` with:
   - SQLAlchemy Base import from core.database
   - Todo class with all required fields and constraints
   - Table name: `todos`
   - Proper column types, constraints, and defaults
   - Index definitions (if any)

**Files to Create**:
- `backend/models/database_todo.py` (new file, separate from Pydantic models)

**Model Specifications**:
```python
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(500), nullable=False)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
```

**Acceptance Criteria**:
- [ ] Todo class inherits from Base
- [ ] All required columns defined with correct types
- [ ] Constraints applied (nullable, max length, defaults)
- [ ] Model can be imported without errors
- [ ] Model metadata accessible via `Todo.metadata`

**Manual Commands**: None

---

### Phase 3: Alembic Configuration

**Objective**: Ensure Alembic is properly configured to work with async SQLAlchemy.

**Tasks**:
1. Review and update `backend/alembic/env.py`:
   - Verify Base import from core.database
   - Verify Todo model import from models.database_todo
   - Verify async engine configuration
   - Verify database URL from environment (not .env file reading)

2. Review `backend/alembic.ini`:
   - Ensure script_location points to alembic directory
   - Ensure version_locations is correct
   - SQLAlchemy URL can be overridden via env.py

**Files to Modify**:
- `backend/alembic/env.py` (update imports if necessary)
- `backend/alembic.ini` (verify configuration, may not need changes)

**Acceptance Criteria**:
- [ ] env.py imports Base from core.database (not database module)
- [ ] env.py imports Todo from models.database_todo
- [ ] Alembic can connect to database using environment configuration
- [ ] env.py handles async migrations correctly

**Manual Commands**: None

---

### Phase 4: Initial Migration

**Objective**: Generate and apply the initial database schema migration.

**Tasks**:
1. Generate initial migration file
2. Review migration SQL for correctness
3. Apply migration to create todos table

**Files Generated**:
- `backend/alembic/versions/<timestamp>_<revision>_initial_migration.py`

**Manual Commands**:
```bash
# From backend directory:
alembic revision --autogenerate -m "Initial todos table creation"
alembic upgrade head
```

**Acceptance Criteria**:
- [ ] Migration file generated without errors
- [ ] Migration file creates todos table with correct schema
- [ ] Migration file includes proper downgrade function
- [ ] `alembic upgrade head` executes successfully
- [ ] Todos table exists in PostgreSQL database
- [ ] Table schema matches SQLAlchemy model definition

---

### Phase 5: Service Layer Migration

**Objective**: Update todo_service.py to use database sessions instead of in-memory storage.

**Tasks**:
1. Replace in-memory storage imports with database imports
2. Add db: AsyncSession parameter to all service methods
3. Implement create_todo using async SQLAlchemy
4. Implement list_todos using async SQLAlchemy
5. Implement get_todo using async SQLAlchemy
6. Implement update_todo using async SQLAlchemy
7. Implement delete_todo using async SQLAlchemy
8. Remove in-memory storage (todos list and next_id counter)

**Files to Modify**:
- `backend/services/todo_service.py` (complete rewrite)

**Service Method Specifications**:
```python
def create_todo(description: str, db: AsyncSession) -> TodoResponse:
    # Create Todo ORM instance
    # Add to session
    # Commit transaction
    # Refresh to get database-generated values
    # Return TodoResponse

async def list_todos(db: AsyncSession) -> List[TodoResponse]:
    # Query all todos
    # Return list of TodoResponse

async def get_todo(todo_id: int, db: AsyncSession) -> TodoResponse:
    # Query by id
    # Raise HTTPException 404 if not found
    # Return TodoResponse

async def update_todo(todo_id: int, description: Optional[str], completed: Optional[bool], db: AsyncSession) -> TodoResponse:
    # Query by id
    # Raise HTTPException 404 if not found
    # Update fields if provided
    # Commit transaction
    # Refresh and return TodoResponse

async def delete_todo(todo_id: int, db: AsyncSession) -> None:
    # Query by id
    # Raise HTTPException 404 if not found
    # Delete from session
    # Commit transaction
```

**Acceptance Criteria**:
- [ ] All service methods are async (use await for database operations)
- [ ] All methods accept db: AsyncSession parameter
- [ ] create_todo creates Todo in database and returns TodoResponse
- [ ] list_todos returns all todos from database
- [ ] get_todo returns single todo or raises 404
- [ ] update_todo modifies todo in database and returns updated TodoResponse
- [ ] delete_todo removes todo from database or raises 404
- [ ] All database operations within transaction context
- [ ] In-memory storage (todos list, next_id) removed

**Manual Commands**: None

---

### Phase 6: Route Layer Updates

**Objective**: Update route handlers to inject database dependency into service methods.

**Tasks**:
1. Import Depends from fastapi
2. Import get_db from core.database
3. Update all route handlers to pass db: AsyncSession to service methods

**Files to Modify**:
- `backend/routes/todos.py`

**Route Handler Changes**:
```python
# Example for create_todo:
@router.post(...)
async def create_todo(data: TodoCreate, db: AsyncSession = Depends(get_db)):
    todo = await todo_service.create_todo(data.description, db)
    return TodoResponse(**todo)
```

**Acceptance Criteria**:
- [ ] All route handlers use Depends(get_db) for database session
- [ ] Database session passed to all service method calls
- [ ] Service method results converted to TodoResponse as before
- [ ] API contract remains unchanged (no breaking changes)

**Manual Commands**: None

---

### Phase 7: Testing and Validation

**Objective**: Verify the implementation meets all acceptance criteria from the specification.

**Tasks**:
1. Start application and verify database connection
2. Test create todo endpoint
3. Test list todos endpoint
4. Test get todo endpoint
5. Test update todo endpoint
6. Test delete todo endpoint
7. Verify data persistence after application restart
8. Verify validation (empty description, max length 500)
9. Verify timestamp behavior (created_at, updated_at)

**Manual Commands**:
```bash
# Start application:
uvicorn main:app --reload

# Run API tests (using curl or frontend):
curl -X POST http://localhost:8000/api/todos -H "Content-Type: application/json" -d '{"description": "Test todo"}'
curl http://localhost:8000/api/todos
curl http://localhost:8000/api/todos/1
curl -X PATCH http://localhost:8000/api/todos/1 -H "Content-Type: application/json" -d '{"completed": true}'
curl -X DELETE http://localhost:8000/api/todos/1

# Restart application and verify data persists
```

**Acceptance Criteria**:
- [ ] Application starts without database connection errors
- [ ] Create todo persists in database
- [ ] List todos returns all todos from database
- [ ] Get todo returns single todo or 404
- [ ] Update todo modifies database record
- [ ] Delete todo removes record from database
- [ ] Data persists after application restart
- [ ] Empty description returns 400 error
- [ ] Description > 500 characters returns 400 error
- [ ] Timestamps are set correctly (created_at on create, updated_at on update)

---

## Final Folder Structure

```
backend/
├── alembic/
│   ├── versions/
│   │   └── <timestamp>_<revision>_initial_migration.py  # New migration file
│   └── env.py                                          # Updated (imports)
├── core/
│   ├── config.py                                       # Existing
│   └── database.py                                     # New - database connection
├── models/
│   ├── __init__.py                                     # Existing
│   ├── todo.py                                         # Existing - Pydantic models
│   └── database_todo.py                                # New - SQLAlchemy ORM model
├── routes/
│   ├── __init__.py                                     # Existing
│   └── todos.py                                        # Updated - database dependency
├── services/
│   ├── __init__.py                                     # Existing
│   └── todo_service.py                                 # Updated - database operations
├── alembic.ini                                         # Existing - reviewed
├── main.py                                             # Existing
└── pyproject.toml                                      # Existing
```

---

## Manual Commands Summary

The user needs to run the following commands during implementation:

### Phase 4 - Migration Generation and Application

From the `backend/` directory:

```bash
# Generate initial migration
alembic revision --autogenerate -m "Initial todos table creation"

# Apply migration to create table
alembic upgrade head
```

### Phase 7 - Testing

```bash
# Start application for testing
uvicorn main:app --reload

# Optional: Check migration status
alembic current

# Optional: Show migration history
alembic history
```

---

## Risk Analysis and Mitigation

### Risk 1: Database Connection Failure on Startup
**Likelihood**: Medium
**Impact**: High - Application cannot start

**Mitigation**:
- Provide clear error messages for connection failures
- Document database setup requirements
- Include health check endpoint that verifies database connectivity

**Fallback**: Application logs connection error and fails fast

---

### Risk 2: Migration Conflicts with Existing Database
**Likelihood**: Low (initial migration on new database)
**Impact**: High - Migration fails, blocks deployment

**Mitigation**:
- Use `alembic history` to check current migration state
- Use `alembic current` to verify database version
- Manual database reset if needed (for development only)

**Fallback**: Manual SQL intervention to align schema

---

### Risk 3: Breaking Frontend API Contract
**Likelihood**: Low (careful maintenance of Pydantic models)
**Impact**: High - Frontend functionality breaks

**Mitigation**:
- Keep Pydantic TodoResponse model unchanged
- Maintain exact same JSON response format
- Test frontend integration before merging

**Fallback**: Revert service layer changes, restore in-memory storage

---

### Risk 4: Async/await Errors in Service Layer
**Likelihood**: Medium
**Impact**: Medium - API calls fail with runtime errors

**Mitigation**:
- Thorough code review for proper async/await usage
- Use linter/mypy to catch async errors
- Test all endpoints with concurrent requests

**Fallback**: Add proper error handling and logging

---

### Risk 5: Performance Degradation with Large Dataset
**Likelihood**: Medium (only under load with many todos)
**Impact**: Low (can be addressed later with indexing)

**Mitigation**:
- Add index on id (primary key, automatic)
- Add index on created_at for future date queries
- Monitor query performance during testing

**Fallback**: Add database indexes as needed (non-blocking change)

---

## Evaluation and Validation

### Definition of Done
- [ ] All phases completed per acceptance criteria
- [ ] Initial migration generated and applied successfully
- [ ] All service methods use database sessions
- [ ] All routes pass database dependency to services
- [ ] Application starts and connects to database
- [ ] API endpoints return correct responses
- [ ] Data persists across application restarts
- [ ] Validation rules enforced (description length, not empty)
- [ ] Timestamps set correctly on create and update
- [ ] No errors in application logs
- [ ] Frontend integration verified (no breaking changes)

### Output Validation
- **Format**: All code follows Python 3.13+ syntax with type hints
- **Requirements**: All functional requirements from spec.md addressed
- **Performance**: All CRUD operations complete within 2 seconds (tested manually)
- **Security**: No database credentials in code, no .env file access
- **Compatibility**: API contract unchanged, frontend works without modification

---

## Follow-ups and Risks

### Immediate Follow-ups (Post-Implementation)
- Update project documentation to reflect database integration
- Add database setup instructions to README
- Consider adding docker-compose for local development database

### Future Enhancements
- Add database indexing based on query patterns
- Implement connection pooling configuration
- Add database query logging for development
- Consider adding soft delete pattern
- Implement database backup strategy
- Add integration tests with test database

### Known Limitations
- No user-scoped todos (all todos shared globally)
- No pagination for large todo lists (future optimization)
- No search or filtering capabilities (future enhancement)
- No audit trail beyond timestamps (future enhancement)
