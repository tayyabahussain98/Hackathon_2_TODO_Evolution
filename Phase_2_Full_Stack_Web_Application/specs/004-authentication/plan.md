# Implementation Plan: Better Auth Authentication with JWT and OAuth

**Branch**: `004-authentication` | **Date**: 2025-12-30 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/004-authentication/spec.md`

## Summary

Add secure authentication to the full-stack Todo app using Better Auth with email/password login, Google OAuth support, JWT-based sessions, user-specific todos, protected API routes, and protected frontend pages. Transform the application from global shared todos to a multi-tenant system with complete user data isolation.

**Key Change**: Add authentication layer and scope all todos to authenticated users.

## Technical Context

**Language/Version**: Python 3.13 (backend), TypeScript/React 18+ (frontend)
**Primary Dependencies**:
- Backend: FastAPI, Better Auth FastAPI plugin, python-jose, passlib[bcrypt], SQLAlchemy
- Frontend: Next.js 14+, Better Auth React SDK, ShadCN/UI
**Storage**: PostgreSQL (existing) - add users, session_tokens tables, user_id to todos
**Testing**: Manual testing via curl and frontend (automated tests out of scope for MVP)
**Target Platform**: Linux server (backend), Web browsers (frontend)
**Project Type**: Web application (backend + frontend)
**Performance Goals**: < 2s response time for auth operations, 100 concurrent users
**Constraints**:
- NEVER access or display .env file contents
- Maintain backward compatibility with existing todo API
- Must use Better Auth for OAuth integration
**Scale/Scope**: MVP for 100 users, expandable to 10k+ users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Layer Separation (Section II)
- ✅ Routes handle HTTP only: Auth routes in backend/routes/auth.py, todo routes remain thin
- ✅ Services contain business logic: auth_service.py, jwt_service.py, oauth_service.py
- ✅ Models define data shape: User, SessionToken, Todo (modified) models
- ✅ Middleware handles auth: get_current_user dependency for JWT validation
- ✅ No SQL queries in routes: All queries in services layer
- ✅ Frontend API centralized: All auth calls through lib/api.ts

### Backend Architecture (Section III)
- ✅ Thin controllers: Auth routes delegate to auth_service
- ✅ Business logic in services: Password hashing, JWT generation, user validation
- ✅ Data contracts: Pydantic models for auth requests/responses
- ✅ Middleware: JWT validation middleware for protected routes
- ✅ Database queries in services: User lookup, session management in auth_service

### Frontend Architecture (Section IV)
- ✅ Reusable components: LogoutButton, AuthProvider components
- ✅ Centralized API: All auth calls through lib/api.ts with Authorization header
- ✅ No business logic in components: Auth state managed by context/hooks
- ✅ No direct database access: All data via backend API

### Authentication Architecture (Section V)
- ✅ JWT tokens: Stateless session management with 24-hour expiration
- ✅ Better Auth integration: Email & Password + Google OAuth providers
- ✅ Secrets in environment: BETTER_AUTH_SECRET, JWT_SECRET, GOOGLE_CLIENT_ID/SECRET
- ✅ No hardcoded secrets: All via environment variables
- ✅ No plaintext passwords: bcrypt hashing with work factor 12

### Database Architecture (Section VI)
- ✅ Schema changes via migrations: Alembic migrations for users, session_tokens, todos.user_id
- ✅ Reversible migrations: All migrations include upgrade() and downgrade()
- ✅ SQLAlchemy ORM: User, SessionToken models defined
- ✅ Foreign keys defined: user_id foreign key to users table
- ✅ No manual schema changes: All via Alembic

### Spec-Driven Workflow (Section I)
- ✅ Specification exists: specs/004-authentication/spec.md approved
- ✅ Planning phase: This plan.md follows template
- ✅ Tasks breakdown: Will follow with /sp.tasks command
- ✅ Implementation: Will follow tasks.md
- ✅ No shortcuts: Following complete workflow

**GATE STATUS**: ✅ PASS - All constitution checks satisfied, no violations

## Project Structure

### Documentation (this feature)

```
specs/004-authentication/
├── spec.md              # Approved specification
├── plan.md              # This file
├── research.md          # Phase 0 output (Better Auth patterns, JWT best practices)
├── data-model.md        # Phase 1 output (User, SessionToken, Todo entities)
├── contracts/           # Phase 1 output (Auth API contracts)
│   ├── auth-signup.yaml
│   ├── auth-login.yaml
│   ├── auth-logout.yaml
│   └── auth-oauth.yaml
├── quickstart.md        # Phase 1 output (Auth flow testing scenarios)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```
backend/
├── alembic/
│   └── versions/
│       ├── 20251229_001_initial_todos.py (existing)
│       ├── <timestamp>_002_add_users_session_tokens.py (NEW)
│       └── <timestamp>_003_add_user_id_to_todos.py (NEW)
├── core/
│   ├── config.py (UPDATED - add auth settings)
│   ├── database.py (existing)
│   └── auth_config.py (NEW - Better Auth configuration)
├── models/
│   ├── todo.py (existing - Pydantic)
│   ├── database_todo.py (UPDATED - add user_id field)
│   ├── user.py (NEW - SQLAlchemy User model)
│   ├── session_token.py (NEW - SQLAlchemy SessionToken model)
│   └── auth.py (NEW - Pydantic auth request/response models)
├── routes/
│   ├── todos.py (UPDATED - add auth dependency)
│   └── auth.py (NEW - signup, login, logout, OAuth endpoints)
├── services/
│   ├── todo_service.py (UPDATED - add user_id filtering)
│   ├── auth_service.py (NEW - password hashing, user creation)
│   ├── jwt_service.py (NEW - JWT generation and validation)
│   └── oauth_service.py (NEW - Google OAuth handling)
├── middleware/
│   └── auth_middleware.py (NEW - get_current_user dependency)
├── main.py (UPDATED - include auth router)
└── pyproject.toml (UPDATED - add dependencies)

frontend/
├── lib/
│   ├── api.ts (UPDATED - add Authorization header)
│   └── auth/
│       ├── tokenStorage.ts (NEW - localStorage utilities)
│       └── AuthContext.tsx (NEW - auth state management)
├── hooks/
│   └── useAuth.ts (NEW - auth hook)
├── components/
│   └── LogoutButton.tsx (NEW - logout component)
├── app/
│   ├── login/
│   │   └── page.tsx (NEW - login page)
│   ├── signup/
│   │   └── page.tsx (NEW - signup page)
│   ├── auth/
│   │   └── callback/
│   │       └── google/
│   │           └── page.tsx (NEW - OAuth callback)
│   ├── layout.tsx (UPDATED - wrap with AuthProvider)
│   └── page.tsx (UPDATED - add auth redirect)
└── package.json (UPDATED - add dependencies)
```

**Structure Decision**: Web application monorepo with backend/ and frontend/ separation. Backend follows FastAPI conventions (routes, services, models, middleware). Frontend follows Next.js 14 App Router structure.

## Complexity Tracking

No constitution violations requiring justification.

---

## Phase 0: Research & Design Decisions

**Objective**: Resolve technical unknowns and document authentication patterns

### Research Topics

1. **Better Auth Integration Patterns**
   - How Better Auth integrates with FastAPI
   - Better Auth Email & Password provider configuration
   - Better Auth Google OAuth provider setup
   - Session management vs JWT-only approach

2. **JWT Best Practices**
   - Token structure and claims (sub, email, exp, iat, iss)
   - Secret key management and rotation
   - Token expiration strategy (access vs refresh tokens)
   - Token storage (localStorage vs httpOnly cookies)

3. **User Data Isolation**
   - Foreign key relationships (user_id in todos)
   - Database-level filtering patterns
   - Ownership verification strategies
   - Migration strategy for existing todos

4. **OAuth Security**
   - State parameter for CSRF protection
   - Authorization code exchange flow
   - Account linking vs creation logic
   - Redirect URL configuration

### Research Outputs

**research.md** will document:
- **Decision**: Use Better Auth for OAuth, custom JWT for API sessions
- **Rationale**: Better Auth handles OAuth complexity, custom JWT provides control
- **Alternatives**: Pure OAuth2 (too complex), Auth0 (external dependency), custom only (reinventing wheel)

**Decision**: Use localStorage for token storage (MVP), migrate to httpOnly cookies later
- **Rationale**: Simpler frontend integration, explicit upgrade path
- **Alternatives**: httpOnly cookies (requires CSRF protection), sessionStorage (poor UX)

**Decision**: Database-backed session tokens for revocation
- **Rationale**: Enable logout functionality, session cleanup
- **Alternatives**: Stateless JWT only (cannot revoke), Redis (additional infrastructure)

**Acceptance Criteria**:
- [ ] All NEEDS CLARIFICATION items resolved
- [ ] Better Auth integration pattern documented
- [ ] JWT structure defined
- [ ] User isolation strategy documented
- [ ] OAuth security patterns documented

---

## Phase 1: Data Model & Contracts

**Objective**: Define database schema and API contracts

### Data Model

**data-model.md** will define:

**User Entity**:
- id: Integer, primary key, auto-increment
- email: String(255), unique, indexed, not null
- password_hash: String(255), not null
- google_id: String(255), unique, nullable
- created_at: DateTime, default now()
- updated_at: DateTime, default now(), onupdate now()

**SessionToken Entity**:
- id: Integer, primary key, auto-increment
- user_id: Integer, foreign key to users.id, cascade delete
- token: Text, unique, not null
- expires_at: DateTime, not null
- created_at: DateTime, default now()

**Todo Entity (Modified)**:
- (existing fields unchanged)
- user_id: Integer, foreign key to users.id, cascade delete, nullable initially

**Relationships**:
- User → SessionToken: One-to-many
- User → Todo: One-to-many
- Todo → User: Many-to-one

### API Contracts

**contracts/** will include:

**auth-signup.yaml**:
```yaml
POST /api/auth/signup:
  request:
    email: string (format: email)
    password: string (minLength: 8)
  response:
    access_token: string
    token_type: "bearer"
    expires_in: 86400
    user:
      id: integer
      email: string
  errors:
    400: Invalid email or password format
    409: Email already exists
    500: Server error
```

**auth-login.yaml**:
```yaml
POST /api/auth/login:
  request:
    email: string
    password: string
  response:
    access_token: string
    token_type: "bearer"
    expires_in: 86400
    user:
      id: integer
      email: string
  errors:
    401: Invalid credentials
    500: Server error
```

**auth-logout.yaml**:
```yaml
POST /api/auth/logout:
  headers:
    Authorization: Bearer <token>
  response:
    message: "Logged out successfully"
  errors:
    401: Invalid token
```

**auth-oauth-google.yaml**:
```yaml
GET /api/auth/google/login:
  response:
    redirect: Google OAuth consent URL

GET /api/auth/google/callback:
  query:
    code: string
    state: string
  response:
    HTML with postMessage containing JWT token
  errors:
    400: Invalid state or code
    401: OAuth failed
```

### Quickstart

**quickstart.md** will include:

1. **Setup**: Install dependencies, configure environment
2. **Signup Flow**: POST /api/auth/signup → receive token
3. **Login Flow**: POST /api/auth/login → receive token
4. **Protected Request**: GET /api/todos with Authorization header
5. **Logout Flow**: POST /api/auth/logout → token invalidated
6. **OAuth Flow**: Click Google button → OAuth flow → receive token
7. **Data Isolation**: Create todo as User A, verify User B cannot access

**Acceptance Criteria**:
- [ ] data-model.md complete with all entities
- [ ] All API contracts documented in contracts/
- [ ] quickstart.md provides end-to-end testing scenarios

---

## Phase 2: Implementation Planning

**Prerequisites**: research.md and data-model.md complete

### Dependency Installation

**Backend** (from backend directory):
```bash
uv add python-jose[cryptography]
uv add passlib[bcrypt]
uv add python-multipart
```

**Frontend** (from frontend directory):
```bash
npm install axios
```

**Note**: Better Auth is NOT used based on research findings. We're implementing custom JWT authentication with optional Google OAuth using standard libraries.

### Database Changes

**Migration 1**: Add users and session_tokens tables
**Migration 2**: Add user_id to todos table

**Users Table Schema**:
```python
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    google_id: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
```

**SessionToken Table Schema**:
```python
class SessionToken(Base):
    __tablename__ = "session_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token: Mapped[str] = mapped_column(Text, unique=True, nullable=False, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
```

**Todo Table Update**:
```python
# Add to existing Todo model:
user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
```

### Backend Authentication Setup

**Core Configuration** (`backend/core/auth_config.py`):
```python
class AuthSettings(BaseSettings):
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    bcrypt_rounds: int = 12
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    oauth_redirect_uri: str = "http://localhost:3000/auth/callback/google"
```

**Authentication Services**:
- `auth_service.py`: create_user(), authenticate_user(), hash_password(), verify_password()
- `jwt_service.py`: create_access_token(), decode_access_token(), create_session_token(), delete_session_token()
- `oauth_service.py`: google_oauth_login(), google_oauth_callback(), link_google_account()

**Authentication Routes** (`backend/routes/auth.py`):
- POST /api/auth/signup
- POST /api/auth/login
- POST /api/auth/logout
- GET /api/auth/google/login
- GET /api/auth/google/callback

**Authentication Middleware** (`backend/middleware/auth_middleware.py`):
- get_current_user() - FastAPI dependency that validates JWT and returns User

### Frontend Authentication Setup

**Token Storage** (`frontend/lib/auth/tokenStorage.ts`):
```typescript
export const saveToken = (token: string) => localStorage.setItem('auth_token', token);
export const getToken = () => localStorage.getItem('auth_token');
export const removeToken = () => localStorage.removeItem('auth_token');
```

**Auth Context** (`frontend/lib/auth/AuthContext.tsx`):
```typescript
interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string) => Promise<void>;
  logout: () => void;
  loginWithGoogle: () => void;
  isAuthenticated: boolean;
}
```

**Auth Hook** (`frontend/hooks/useAuth.ts`):
- Provides access to auth context
- Handles token validation on mount
- Auto-redirects on token expiration

**Auth Pages**:
- `app/login/page.tsx`: Email/password login form + Google OAuth button
- `app/signup/page.tsx`: Email/password signup form + Google OAuth button
- `app/auth/callback/google/page.tsx`: OAuth callback handler

### Protected Routes Implementation

**Backend** (`backend/routes/todos.py`):
```python
from middleware.auth_middleware import get_current_user
from models.user import User

@router.post("/api/todos", dependencies=[Depends(get_current_user)])
async def create_todo(
    data: TodoCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    todo = await todo_service.create_todo(data.description, current_user.id, db)
    return TodoResponse(**todo)
```

**Frontend** (`frontend/lib/api.ts`):
```typescript
import { getToken } from './auth/tokenStorage';

export const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to all requests
apiClient.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### Protected Pages Implementation

**Frontend** (`frontend/app/page.tsx`):
```typescript
'use client';

import { useAuth } from '@/hooks/useAuth';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function HomePage() {
  const { isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  if (!isAuthenticated) {
    return null; // Or loading spinner
  }

  return (
    // Existing todo UI
  );
}
```

### Session/JWT Management

**JWT Token Generation** (`backend/services/jwt_service.py`):
```python
def create_access_token(user_id: int, email: str) -> str:
    payload = {
        "sub": str(user_id),
        "email": email,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=24),
        "iss": "todo-app"
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
```

**JWT Token Validation** (`backend/middleware/auth_middleware.py`):
```python
async def get_current_user(
    authorization: str = Header(None),
    db: AsyncSession = Depends(get_db)
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = authorization.split(" ")[1]

    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        user_id = int(payload.get("sub"))
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user
```

---

## Implementation Phases (Step-by-Step)

### Phase 1: Backend Better Auth Setup

**Objective**: Install dependencies and create authentication infrastructure

**Tasks**:
1. Add dependencies to backend/pyproject.toml
2. Create backend/core/auth_config.py with authentication settings
3. Create backend/models/user.py with User SQLAlchemy model
4. Create backend/models/session_token.py with SessionToken SQLAlchemy model
5. Update backend/alembic/env.py to import User and SessionToken models

**Files to Create**:
- backend/core/auth_config.py
- backend/models/user.py
- backend/models/session_token.py
- backend/models/auth.py (Pydantic models)

**Files to Modify**:
- backend/pyproject.toml
- backend/alembic/env.py
- backend/core/config.py

**Acceptance Criteria**:
- [ ] Dependencies installed (python-jose, passlib, python-multipart)
- [ ] User model created with all fields
- [ ] SessionToken model created with foreign key
- [ ] Auth settings loaded from environment
- [ ] Models import without errors

**Manual Commands**:
```bash
cd backend
uv add python-jose[cryptography]
uv add passlib[bcrypt]
uv add python-multipart
```

---

### Phase 2: Database Migration for Users and Sessions

**Objective**: Generate and apply Alembic migrations for authentication tables

**Tasks**:
1. Generate migration for users and session_tokens tables
2. Review migration SQL for correctness
3. Apply migration to database

**Acceptance Criteria**:
- [ ] Migration file generated successfully
- [ ] users table created with all fields and indexes
- [ ] session_tokens table created with foreign key
- [ ] Migration applied without errors
- [ ] Tables exist in PostgreSQL database

**Manual Commands**:
```bash
cd backend
.venv/bin/python -m alembic revision --autogenerate -m "Add users and session_tokens tables"
.venv/bin/python -m alembic upgrade head
```

---

### Phase 3: User Story 1 - Email/Password Authentication (Priority: P1) 🎯 MVP

**Objective**: Implement signup, login, and logout functionality

**Backend Tasks**:
1. Create backend/services/auth_service.py with password hashing and user management
2. Create backend/services/jwt_service.py with JWT generation and validation
3. Create backend/routes/auth.py with signup, login, logout endpoints
4. Update backend/main.py to include auth router

**Service Functions**:

**auth_service.py**:
- `async def create_user(email: str, password: str, db: AsyncSession) -> User`
- `async def authenticate_user(email: str, password: str, db: AsyncSession) -> Optional[User]`
- `def hash_password(password: str) -> str`
- `def verify_password(plain_password: str, hashed_password: str) -> bool`

**jwt_service.py**:
- `def create_access_token(user_id: int, email: str) -> str`
- `def decode_access_token(token: str) -> dict`
- `async def create_session_token(user_id: int, token: str, db: AsyncSession) -> SessionToken`
- `async def delete_session_token(token: str, db: AsyncSession) -> None`

**Route Endpoints**:
- POST /api/auth/signup - Create user, hash password, generate JWT, store session
- POST /api/auth/login - Validate credentials, generate JWT, store session
- POST /api/auth/logout - Delete session token from database

**Acceptance Criteria**:
- [ ] Signup creates user with bcrypt-hashed password
- [ ] Signup returns JWT token with 24-hour expiration
- [ ] Login validates credentials correctly
- [ ] Login returns 401 for invalid credentials
- [ ] Logout deletes session token
- [ ] JWT tokens have correct structure (sub, email, exp, iat, iss)
- [ ] All responses follow API contract

**Manual Commands**: None (code implementation only)

---

### Phase 4: User Story 3 - Protected API Routes (Priority: P1)

**Objective**: Add JWT validation middleware and protect todo endpoints

**Backend Tasks**:
1. Create backend/middleware/auth_middleware.py with get_current_user dependency
2. Update backend/routes/todos.py to require authentication
3. Update backend/services/todo_service.py to accept user_id parameter
4. Update backend/models/database_todo.py to add user_id field

**Middleware Implementation**:
```python
async def get_current_user(
    authorization: str = Header(None),
    db: AsyncSession = Depends(get_db)
) -> User:
    # Extract and validate JWT token
    # Return User or raise 401/403
```

**Todo Service Updates**:
- All methods now accept `user_id: int` parameter
- list_todos(): Filter WHERE user_id = ?
- create_todo(): Set user_id on creation
- get_todo(): Verify ownership or raise 403
- update_todo(): Verify ownership or raise 403
- delete_todo(): Verify ownership or raise 403

**Acceptance Criteria**:
- [ ] All todo endpoints require valid JWT token
- [ ] Missing token returns 401 Unauthorized
- [ ] Invalid token returns 401 Unauthorized
- [ ] Expired token returns 401 Unauthorized
- [ ] User can only access their own todos
- [ ] Accessing another user's todo returns 403 Forbidden
- [ ] User ID extracted from token correctly

**Manual Commands**: None

---

### Phase 5: Database Migration for User-Specific Todos

**Objective**: Add user_id foreign key to todos table

**Tasks**:
1. Generate migration to add user_id column to todos
2. Apply migration

**Acceptance Criteria**:
- [ ] Migration file generated successfully
- [ ] user_id column added to todos table
- [ ] Foreign key constraint created
- [ ] Index created on user_id
- [ ] Existing todos have user_id = NULL (backward compatible)
- [ ] Migration applied without errors

**Manual Commands**:
```bash
cd backend
.venv/bin/python -m alembic revision --autogenerate -m "Add user_id to todos table"
.venv/bin/python -m alembic upgrade head
```

---

### Phase 6: User Story 4 - Protected Frontend Pages (Priority: P1)

**Objective**: Add authentication state management and protected page redirects

**Frontend Tasks**:
1. Create frontend/lib/auth/tokenStorage.ts - localStorage utilities
2. Create frontend/lib/auth/AuthContext.tsx - Auth context provider
3. Create frontend/hooks/useAuth.ts - Auth state hook
4. Create frontend/app/login/page.tsx - Login page
5. Create frontend/app/signup/page.tsx - Signup page
6. Update frontend/lib/api.ts - Add Authorization header to all requests
7. Update frontend/app/page.tsx - Add auth redirect logic
8. Create frontend/components/LogoutButton.tsx - Logout component
9. Update frontend/app/layout.tsx - Wrap with AuthProvider

**Auth Context Implementation**:
- Provides user, token, login, signup, logout, isAuthenticated
- Stores token in localStorage
- Validates token on mount
- Auto-redirects on token expiration

**API Client Update**:
- Add interceptor to include Authorization header
- Get token from localStorage
- Format: `Authorization: Bearer <token>`

**Acceptance Criteria**:
- [ ] Unauthenticated users redirected to /login
- [ ] Login page authenticates and stores token
- [ ] Signup page creates account and stores token
- [ ] Token included in all API requests
- [ ] Logout clears token and redirects to /login
- [ ] Token expiration triggers automatic logout
- [ ] Auth state persists across page refreshes

**Manual Commands**:
```bash
cd frontend
npm install axios  # If not already installed
```

---

### Phase 7: User Story 5 - User-Specific Todos Implementation

**Objective**: Ensure all todo operations are scoped to authenticated user

**Backend Tasks**:
1. Update todo service methods to filter by user_id
2. Update todo routes to pass current_user.id to services
3. Add ownership verification for get/update/delete operations
4. Update Pydantic TodoResponse to include user_id field

**Service Method Updates**:
```python
# list_todos
result = await db.execute(select(Todo).where(Todo.user_id == user_id).order_by(Todo.id))

# create_todo
todo = Todo(description=description, user_id=user_id, completed=False)

# get_todo/update_todo/delete_todo
if todo.user_id != user_id:
    raise HTTPException(status_code=403, detail="Access denied")
```

**Acceptance Criteria**:
- [ ] Create todo automatically sets user_id
- [ ] List todos returns only current user's todos
- [ ] Get todo verifies ownership (403 if mismatch)
- [ ] Update todo verifies ownership (403 if mismatch)
- [ ] Delete todo verifies ownership (403 if mismatch)
- [ ] Two users cannot see each other's todos
- [ ] TodoResponse includes user_id field

**Manual Commands**: None

---

### Phase 8: User Story 2 - Google OAuth Authentication (Priority: P2)

**Objective**: Add Google OAuth login/signup flow (optional, ready for configuration)

**Backend Tasks**:
1. Create backend/services/oauth_service.py with Google OAuth handlers
2. Update backend/routes/auth.py to add Google OAuth endpoints
3. Add OAuth state parameter generation and validation

**Frontend Tasks**:
1. Update frontend/app/login/page.tsx - Add "Sign in with Google" button
2. Update frontend/app/signup/page.tsx - Add "Sign up with Google" button
3. Create frontend/app/auth/callback/google/page.tsx - OAuth callback handler
4. Update frontend/hooks/useAuth.ts - Add loginWithGoogle() function

**OAuth Flow**:
1. User clicks "Sign in with Google"
2. Frontend calls GET /api/auth/google/login
3. Backend redirects to Google OAuth consent screen (with state parameter)
4. User authorizes application on Google
5. Google redirects to /api/auth/google/callback?code=...&state=...
6. Backend validates state, exchanges code for user info
7. Backend creates/links user account, generates JWT
8. Backend returns HTML with postMessage to parent window
9. Frontend receives token, stores in localStorage

**Acceptance Criteria**:
- [ ] Google OAuth flow completes successfully
- [ ] State parameter validated (CSRF protection)
- [ ] New Google users created in database
- [ ] Existing email users linked to Google account
- [ ] JWT token issued after OAuth
- [ ] OAuth errors handled gracefully
- [ ] Callback page sends token to parent window

**Manual Commands**:
User must configure Google OAuth credentials in environment (not .env file directly)

---

### Phase 9: Testing & Validation

**Objective**: Comprehensive end-to-end testing of all authentication flows

**Manual Testing Scenarios**:

**Email/Password Flow**:
```bash
# Signup
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123!"}'

# Expected: 201 Created with access_token

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123!"}'

# Expected: 200 OK with access_token

# Access protected endpoint
curl http://localhost:8000/api/todos \
  -H "Authorization: Bearer <token_from_login>"

# Expected: 200 OK with user's todos

# Access without token
curl http://localhost:8000/api/todos

# Expected: 401 Unauthorized

# Logout
curl -X POST http://localhost:8000/api/auth/logout \
  -H "Authorization: Bearer <token>"

# Expected: 200 OK, token invalidated
```

**Data Isolation Testing**:
```bash
# Create User A
curl -X POST http://localhost:8000/api/auth/signup \
  -d '{"email":"userA@example.com","password":"Pass123!"}'
# Save token as TOKEN_A

# Create User B
curl -X POST http://localhost:8000/api/auth/signup \
  -d '{"email":"userB@example.com","password":"Pass123!"}'
# Save token as TOKEN_B

# User A creates todo
curl -X POST http://localhost:8000/api/todos \
  -H "Authorization: Bearer $TOKEN_A" \
  -d '{"description":"User A todo"}'
# Returns todo with id=1

# User B lists todos
curl http://localhost:8000/api/todos \
  -H "Authorization: Bearer $TOKEN_B"
# Expected: Empty array (User B has no todos)

# User B attempts to access User A's todo
curl http://localhost:8000/api/todos/1 \
  -H "Authorization: Bearer $TOKEN_B"
# Expected: 403 Forbidden
```

**Frontend Testing**:
1. Visit http://localhost:3000/ without auth → redirected to /login
2. Sign up with email/password → redirected to /
3. Create todos → persist to database
4. Refresh page → todos still visible (token from localStorage)
5. Logout → token cleared, redirected to /login
6. Visit / → redirected to /login (not authenticated)
7. Login with Google OAuth → redirected to / (if Google configured)

**Acceptance Criteria**:
- [ ] All email/password flows work end-to-end
- [ ] All protected endpoints require authentication
- [ ] Data isolation verified (users cannot see others' todos)
- [ ] Frontend redirects work correctly
- [ ] Token stored and retrieved from localStorage
- [ ] Logout clears token completely
- [ ] OAuth flow completes (if Google configured)
- [ ] No security vulnerabilities identified

**Manual Commands**: See curl commands above

---

## Final Folder Structure

```
backend/
├── alembic/
│   ├── versions/
│   │   ├── 20251229_001_initial_todos.py (existing)
│   │   ├── <timestamp>_002_users_session_tokens.py (NEW)
│   │   └── <timestamp>_003_add_user_id_to_todos.py (NEW)
│   └── env.py (UPDATED - import User, SessionToken)
├── core/
│   ├── config.py (UPDATED - add JWT settings)
│   ├── database.py (existing)
│   └── auth_config.py (NEW - auth configuration)
├── models/
│   ├── __init__.py (existing)
│   ├── todo.py (existing - Pydantic)
│   ├── database_todo.py (UPDATED - add user_id)
│   ├── user.py (NEW - SQLAlchemy User)
│   ├── session_token.py (NEW - SQLAlchemy SessionToken)
│   └── auth.py (NEW - Pydantic auth models)
├── routes/
│   ├── __init__.py (existing)
│   ├── todos.py (UPDATED - add auth dependency)
│   └── auth.py (NEW - auth endpoints)
├── services/
│   ├── __init__.py (existing)
│   ├── todo_service.py (UPDATED - user_id filtering)
│   ├── auth_service.py (NEW - password, user management)
│   ├── jwt_service.py (NEW - JWT operations)
│   └── oauth_service.py (NEW - OAuth handling)
├── middleware/
│   └── auth_middleware.py (NEW - get_current_user)
├── main.py (UPDATED - include auth router)
└── pyproject.toml (UPDATED - dependencies)

frontend/
├── lib/
│   ├── api.ts (UPDATED - Authorization header)
│   └── auth/
│       ├── tokenStorage.ts (NEW)
│       └── AuthContext.tsx (NEW)
├── hooks/
│   └── useAuth.ts (NEW)
├── components/
│   └── LogoutButton.tsx (NEW)
├── app/
│   ├── login/
│   │   └── page.tsx (NEW)
│   ├── signup/
│   │   └── page.tsx (NEW)
│   ├── auth/
│   │   └── callback/
│   │       └── google/
│   │           └── page.tsx (NEW)
│   ├── layout.tsx (UPDATED - AuthProvider)
│   └── page.tsx (UPDATED - auth redirect)
└── package.json (UPDATED - axios if needed)
```

---

## Manual Commands Summary

### Phase 1 - Dependencies
```bash
cd backend
uv add python-jose[cryptography] passlib[bcrypt] python-multipart

cd ../frontend
npm install axios  # If not already installed
```

### Phase 2 - Users/Sessions Migration
```bash
cd backend
.venv/bin/python -m alembic revision --autogenerate -m "Add users and session_tokens tables"
.venv/bin/python -m alembic upgrade head
```

### Phase 5 - User ID Migration
```bash
cd backend
.venv/bin/python -m alembic revision --autogenerate -m "Add user_id to todos table"
.venv/bin/python -m alembic upgrade head
```

### Phase 8 - Google OAuth Configuration (Optional, Manual)
**User must manually configure** (not .env file):
1. Create Google OAuth application in Google Cloud Console
2. Get Client ID and Client Secret
3. Add to environment:
   - GOOGLE_CLIENT_ID=your_client_id
   - GOOGLE_CLIENT_SECRET=your_client_secret
4. Configure authorized redirect URI: http://localhost:3000/auth/callback/google

### Phase 9 - Testing
```bash
# Start backend
cd backend
.venv/bin/python -m uvicorn main:app --reload --port 8000

# Start frontend (new terminal)
cd frontend
npm run dev

# Test with curl commands from Phase 9
```

---

## Risk Analysis and Mitigation

### Risk 1: JWT Token Compromise
**Likelihood**: Medium (XSS vulnerability)
**Impact**: CRITICAL (unauthorized access)

**Mitigation**:
- Short token lifetime (24 hours)
- Token revocation via logout endpoint
- HTTPS-only transmission in production
- Content Security Policy headers

**Fallback**: Rotate JWT_SECRET_KEY, force global logout

---

### Risk 2: Password Brute-Force Attacks
**Likelihood**: Medium (common attack)
**Impact**: HIGH (account compromise)

**Mitigation**:
- bcrypt work factor 12 (slow hashing)
- Generic error messages (prevent email enumeration)
- Rate limiting (future enhancement)

**Fallback**: Account lockout after failures (future)

---

### Risk 3: Database Migration Failure
**Likelihood**: Low (tested in development)
**Impact**: HIGH (cannot add users)

**Mitigation**:
- Test migrations in development first
- Review generated SQL
- Backup database before migrations
- Reversible migrations (downgrade tested)

**Fallback**: Rollback using `alembic downgrade -1`

---

### Risk 4: OAuth Configuration Errors
**Likelihood**: Medium (manual configuration)
**Impact**: MEDIUM (OAuth login unavailable)

**Mitigation**:
- Clear documentation for OAuth setup
- OAuth errors handled gracefully
- Email/password auth remains available

**Fallback**: Disable OAuth, use email/password only

---

## Evaluation and Validation

### Definition of Done
- [ ] All 9 phases completed
- [ ] Email/password signup/login/logout working
- [ ] Google OAuth ready (configuration optional)
- [ ] All todo endpoints protected with JWT
- [ ] Frontend authentication complete with redirects
- [ ] User-specific todos fully functional
- [ ] Data isolation verified
- [ ] Database migrations applied
- [ ] No security vulnerabilities
- [ ] Manual testing completed
- [ ] No .env file access occurred

### Output Validation
- **Format**: Python 3.13+ with type hints, TypeScript/React code
- **Requirements**: All 32 functional requirements addressed
- **Performance**: Auth operations < 2 seconds
- **Security**: Passwords hashed, secrets in environment, no .env access
- **Compatibility**: Existing todo API enhanced (not broken)

---

## Follow-ups and Risks

### Immediate Follow-ups (Post-Implementation)
- Add rate limiting on auth endpoints
- Implement password reset flow
- Migrate from localStorage to httpOnly cookies
- Add email verification
- Add refresh token rotation

### Future Enhancements
- Two-factor authentication (2FA)
- Admin role-based access control
- Social login providers (GitHub, Facebook)
- Session device tracking
- Advanced OAuth features

### Known Limitations
- No refresh tokens (must re-login after 24 hours)
- localStorage vulnerable to XSS
- No rate limiting initially
- No email verification
- Generic error messages only

---

## STRICT SECURITY RULE

**NEVER ACCESS OR DISPLAY .env FILE CONTENTS**

All environment variables (JWT_SECRET_KEY, DATABASE_URL, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET) are managed by the user and NEVER accessed, read, displayed, or mentioned by the agent during implementation.

---

**Plan Complete - Ready for /sp.tasks**
