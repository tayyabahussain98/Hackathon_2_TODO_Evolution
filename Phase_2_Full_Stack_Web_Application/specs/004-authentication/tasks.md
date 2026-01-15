
---

description: "Task list for Better Auth authentication feature"
---

# Tasks: Better Auth Authentication with JWT and OAuth

**Input**: Design documents from `/specs/004-authentication/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: NOT requested in specification - manual testing only

**Organization**: Tasks organized by user story to enable independent implementation and testing of each story

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/` at repository root
- **Frontend**: `frontend/` at repository root
- Paths shown below use absolute paths

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Install dependencies and verify environment

- [X] T001 Install backend authentication dependencies using `cd backend && uv add python-jose[cryptography] passlib[bcrypt] python-multipart`
- [X] T002 [P] Install frontend dependencies using `cd frontend && npm install axios` (if not already installed)
- [X] T003 Verify JWT_SECRET_KEY environment variable is configured (must be 32+ characters)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core authentication infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Create backend/core/auth_config.py with AuthSettings class for jwt_secret_key, jwt_algorithm, jwt_expiration_hours, bcrypt_rounds, google_client_id, google_client_secret, oauth_redirect_uri
- [X] T005 [P] Create backend/models/user.py with SQLAlchemy User model (id, email, password_hash, google_id, created_at, updated_at) and email/google_id indexes
- [X] T006 [P] Create backend/models/session_token.py with SQLAlchemy SessionToken model (id, user_id FK, token, expires_at, created_at) and indexes
- [X] T007 [P] Create backend/models/auth.py with Pydantic models (SignupRequest, LoginRequest, AuthResponse, UserResponse)
- [X] T008 Update backend/alembic/env.py to import User and SessionToken models from models.user and models.session_token
- [X] T009 Update backend/core/config.py to add jwt_secret_key, jwt_algorithm, jwt_expiration_hours settings to Settings class
- [X] T010 Generate Alembic migration for users and session_tokens tables using `cd backend && .venv/bin/python -m alembic revision --autogenerate -m "Add users and session_tokens tables"`
- [X] T011 Apply migration using `cd backend && .venv/bin/python -m alembic upgrade head`

**Checkpoint**: Foundation ready - User and SessionToken models created, database tables exist

---

## Phase 3: User Story 1 - Email/Password Authentication (Priority: P1) 🎯 MVP

**Goal**: Users can signup, login, and logout with email/password

**Independent Test**: Create account via signup, login with credentials, receive JWT token, logout to invalidate token

### Implementation for User Story 1

- [X] T012 [P] [US1] Create backend/services/auth_service.py with hash_password(), verify_password(), create_user(), and authenticate_user() functions using bcrypt with work factor 12
- [X] T013 [P] [US1] Create backend/services/jwt_service.py with create_access_token(), decode_access_token(), create_session_token(), and delete_session_token() functions
- [X] T014 [US1] Create backend/routes/auth.py with POST /api/auth/signup endpoint that creates user, hashes password, generates JWT, stores session token, and returns AuthResponse
- [X] T015 [US1] Add POST /api/auth/login endpoint to backend/routes/auth.py that validates credentials, generates JWT, stores session token, and returns AuthResponse or 401
- [X] T016 [US1] Add POST /api/auth/logout endpoint to backend/routes/auth.py that deletes session token from database and returns success message
- [X] T017 [US1] Update backend/main.py to include auth router from routes.auth with prefix /api/auth

**Checkpoint**: At this point, User Story 1 should be fully functional - users can signup, login, and logout via API

---

## Phase 4: User Story 3 - Protected API Routes (Priority: P1)

**Goal**: All todo endpoints require valid JWT token and filter by authenticated user

**Independent Test**: Create two users, login as each, create todos, verify each user only sees their own todos and gets 403 when accessing the other's todos

### Implementation for User Story 3

- [X] T018 [US3] Create backend/middleware/auth_middleware.py with get_current_user() async function that extracts JWT from Authorization header, validates token, queries user from database, and returns User or raises 401/403
- [X] T019 [US3] Update backend/models/database_todo.py to add user_id field as Mapped[Optional[int]] with ForeignKey to users.id, cascade delete, nullable=True, and index=True
- [X] T020 [US3] Update backend/services/todo_service.py to add user_id parameter to all functions (create_todo, list_todos, get_todo, update_todo, delete_todo)
- [X] T021 [US3] Update create_todo() in backend/services/todo_service.py to set todo.user_id = user_id when creating Todo instance
- [X] T022 [US3] Update list_todos() in backend/services/todo_service.py to filter query with .where(Todo.user_id == user_id)
- [X] T023 [US3] Update get_todo() in backend/services/todo_service.py to verify todo.user_id == user_id after fetching, raise HTTPException 403 if mismatch
- [X] T024 [US3] Update update_todo() in backend/services/todo_service.py to verify todo.user_id == user_id before updating, raise HTTPException 403 if mismatch
- [X] T025 [US3] Update delete_todo() in backend/services/todo_service.py to verify todo.user_id == user_id before deleting, raise HTTPException 403 if mismatch
- [X] T026 [US3] Update backend/routes/todos.py to import get_current_user from middleware.auth_middleware and User from models.user
- [X] T027 [US3] Update create_todo route in backend/routes/todos.py to add current_user: User = Depends(get_current_user) parameter and pass current_user.id to service
- [X] T028 [US3] Update list_todos route in backend/routes/todos.py to add current_user: User = Depends(get_current_user) parameter and pass current_user.id to service
- [X] T029 [US3] Update get_todo route in backend/routes/todos.py to add current_user: User = Depends(get_current_user) parameter and pass current_user.id to service
- [X] T030 [US3] Update update_todo route in backend/routes/todos.py to add current_user: User = Depends(get_current_user) parameter and pass current_user.id to service
- [X] T031 [US3] Update delete_todo route in backend/routes/todos.py to add current_user: User = Depends(get_current_user) parameter and pass current_user.id to service
- [X] T032 [US3] Update backend/models/todo.py Pydantic TodoResponse to add user_id: int field

**Checkpoint**: At this point, User Story 3 should be fully functional - all todo endpoints require authentication and filter by user_id

---

## Phase 5: Database Migration for User-Specific Todos

**Purpose**: Add user_id foreign key to todos table

- [X] T033 Generate Alembic migration for user_id column using `cd backend && .venv/bin/python -m alembic revision --autogenerate -m "Add user_id to todos table"`
- [X] T034 Apply migration using `cd backend && .venv/bin/python -m alembic upgrade head`

**Checkpoint**: todos table now has user_id foreign key column

---

## Phase 6: User Story 4 - Protected Frontend Pages (Priority: P1)

**Goal**: Frontend redirects unauthenticated users to login page and manages JWT tokens

**Independent Test**: Access homepage without token (redirects to /login), login with credentials (stores token, redirects to /), logout (clears token, redirects to /login)

### Implementation for User Story 4

- [X] T035 [P] [US4] Create frontend/lib/auth/tokenStorage.ts with saveToken(), getToken(), and removeToken() functions for localStorage management
- [X] T036 [P] [US4] Create frontend/lib/auth/AuthContext.tsx with AuthProvider component and AuthContext providing user, token, login, signup, logout, loginWithGoogle, and isAuthenticated
- [X] T037 [P] [US4] Create frontend/hooks/useAuth.ts hook that returns useContext(AuthContext) and validates token on mount
- [X] T038 [US4] Create frontend/app/login/page.tsx with email/password form, login handler calling /api/auth/login, token storage on success, and redirect to homepage
- [X] T039 [US4] Create frontend/app/signup/page.tsx with email/password form, signup handler calling /api/auth/signup, token storage on success, and redirect to homepage
- [X] T040 [US4] Create frontend/components/LogoutButton.tsx with logout handler that calls /api/auth/logout, clears localStorage token, and redirects to /login
- [X] T041 [US4] Update frontend/lib/api.ts to add axios request interceptor that includes Authorization: Bearer <token> header for all requests using getToken()
- [X] T042 [US4] Update frontend/app/layout.tsx to wrap children with AuthProvider component
- [X] T043 [US4] Update frontend/app/page.tsx to add useEffect that checks isAuthenticated and redirects to /login if false using useRouter
- [X] T044 [US4] Add axios response interceptor to frontend/lib/api.ts that handles 401 errors by calling removeToken() and redirecting to /login

**Checkpoint**: At this point, User Story 4 should be fully functional - frontend authentication complete with redirects and token management

---

## Phase 7: User Story 5 - User-Specific Todos (Priority: P1)

**Goal**: All todo operations scoped to authenticated user with ownership verification

**Independent Test**: Create two users, login as each, create todos, verify each user only sees their own todos

### Validation for User Story 5

- [X] T045 [US5] Verify backend/services/todo_service.py filters todos by user_id in list_todos() function (already implemented in T022)
- [X] T046 [US5] Verify backend/services/todo_service.py sets user_id in create_todo() function (already implemented in T021)
- [X] T047 [US5] Verify backend/services/todo_service.py validates ownership in get_todo(), update_todo(), delete_todo() (already implemented in T023-T025)
- [X] T048 [US5] Test data isolation by creating User A, User B, creating todos for each, and verifying each user only sees their own todos

**Checkpoint**: Data isolation verified - users can only CRUD their own todos

---

## Phase 8: User Story 2 - Google OAuth Authentication (Priority: P2)

**Goal**: Users can login/signup with Google OAuth

**Independent Test**: Click "Sign in with Google", complete OAuth flow, receive JWT token, access protected endpoints

### Implementation for User Story 2

- [X] T049 [P] [US2] Create backend/services/oauth_service.py with google_oauth_login(), google_oauth_callback(), and link_google_account() functions
- [X] T050 [US2] Add GET /api/auth/google/login endpoint to backend/routes/auth.py that generates OAuth state parameter and redirects to Google OAuth consent URL
- [X] T051 [US2] Add GET /api/auth/google/callback endpoint to backend/routes/auth.py that validates state, exchanges authorization code for user info, creates/links user account, generates JWT, and returns HTML with postMessage
- [X] T052 [P] [US2] Update frontend/app/login/page.tsx to add "Sign in with Google" button that opens /api/auth/google/login in popup window
- [X] T053 [P] [US2] Update frontend/app/signup/page.tsx to add "Sign up with Google" button that opens /api/auth/google/login in popup window
- [X] T054 [US2] Create frontend/app/auth/callback/google/page.tsx that receives postMessage with token, saves to localStorage, and redirects to homepage
- [X] T055 [US2] Update frontend/hooks/useAuth.ts to add loginWithGoogle() function that opens OAuth popup and handles postMessage response

**Checkpoint**: Google OAuth flow complete - users can login/signup with Google (requires Google OAuth credentials configured)

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Comprehensive testing, validation, and final verification

- [X] T056 Test signup endpoint using `curl -X POST http://localhost:8000/api/auth/signup -H "Content-Type: application/json" -d '{"email":"test@example.com","password":"TestPass123!"}'`
- [X] T057 Test login endpoint using saved email/password credentials from T056
- [X] T058 Test protected todo endpoint with valid token from T057 using `curl http://localhost:8000/api/todos -H "Authorization: Bearer <token>"`
- [X] T059 Test protected todo endpoint without token using `curl http://localhost:8000/api/todos` (should return 401)
- [X] T060 Test logout endpoint using `curl -X POST http://localhost:8000/api/auth/logout -H "Authorization: Bearer <token>"`
- [X] T061 Test data isolation by creating User A and User B, each creating todos, and verifying User A cannot access User B's todos (403 Forbidden)
- [X] T062 Test frontend login page by visiting http://localhost:3000/login and logging in with test credentials
- [X] T063 Test frontend signup page by visiting http://localhost:3000/signup and creating new account
- [X] T064 Test frontend auth redirect by visiting http://localhost:3000/ without token (should redirect to /login)
- [X] T065 Test frontend logout by clicking logout button and verifying token is cleared and redirect to /login occurs
- [X] T066 Test Google OAuth flow (if Google credentials configured) by clicking "Sign in with Google" and completing OAuth flow

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - User Story 1 (Phase 3) implements email/password auth
  - User Story 3 (Phase 4) protects API routes (depends on US1 for JWT validation)
  - User Story 5 (Phase 7) validates user isolation (depends on US3 for ownership checks)
  - User Story 4 (Phase 6) protects frontend pages (depends on US1 for auth endpoints)
  - User Story 2 (Phase 8) adds Google OAuth (depends on US1 for user creation)
- **Polish (Phase 9)**: Depends on all user story phases being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Foundational (Phase 2) - No dependencies on other user stories. Creates auth foundation.
- **User Story 3 (P1)**: Depends on User Story 1 - Requires JWT validation from US1
- **User Story 5 (P1)**: Depends on User Story 3 - Requires protected routes and ownership verification from US3
- **User Story 4 (P1)**: Depends on User Story 1 - Requires auth endpoints from US1
- **User Story 2 (P2)**: Depends on User Story 1 - Requires user creation and JWT generation from US1

### Within Each User Story

- **User Story 1**:
  - T012-T013: Service layer can run in parallel (different files)
  - T014-T016: Route endpoints are sequential (same file)
  - T017: Must complete after routes are created

- **User Story 3**:
  - T018: Middleware creation (prerequisite for routes)
  - T019-T025: Service updates can be done together (same file)
  - T026-T032: Route updates are sequential but can be batched

- **User Story 4**:
  - T035-T037: Can run in parallel (different files)
  - T038-T040: Pages can run in parallel (different files)
  - T041-T044: API updates are sequential (same file)

- **User Story 2**:
  - T049-T051: Backend OAuth can run together
  - T052-T055: Frontend OAuth can run in parallel with backend

### Parallel Opportunities

- T001-T002: Dependency installation can run in parallel (different projects)
- T005-T007: Model creation can run in parallel (different files)
- T012-T013: Auth and JWT services can run in parallel (different files)
- T035-T037: Token storage, context, and hook can run in parallel (different files)
- T038-T040: Login, signup, logout pages/components can run in parallel (different files)
- T049, T052-T053: OAuth backend service and frontend buttons can run in parallel
- T056-T066: All testing tasks can run in parallel

---

## Parallel Example: User Story 1

```bash
# Implement auth services in parallel:
Task: "Create backend/services/auth_service.py with password hashing functions"
Task: "Create backend/services/jwt_service.py with JWT token functions"

# After services complete, add routes sequentially:
Task: "Add POST /api/auth/signup to backend/routes/auth.py"
Task: "Add POST /api/auth/login to backend/routes/auth.py"
Task: "Add POST /api/auth/logout to backend/routes/auth.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 3 + 4)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T011) - CRITICAL
3. Complete Phase 3: User Story 1 (T012-T017) - Email/password auth
4. Complete Phase 4: User Story 3 (T018-T032) - Protected routes
5. Complete Phase 5: Database Migration (T033-T034)
6. Complete Phase 6: User Story 4 (T035-T044) - Protected frontend
7. Complete Phase 7: User Story 5 (T045-T048) - Data isolation validation
8. **STOP and VALIDATE**: Test complete authentication flow end-to-end
9. Deploy/demo if ready

**MVP Delivers**: Users can signup, login, logout, access protected todo endpoints, frontend authentication complete, todos scoped to users.

### Incremental Delivery

1. Complete Setup + Foundational → Auth infrastructure ready
2. Add User Story 1 → Test independently → Email/password auth works
3. Add User Story 3 → Test independently → API routes protected
4. Add User Story 4 → Test independently → Frontend auth complete
5. Add User Story 5 → Test independently → Data isolation verified
6. Add User Story 2 → Test independently → OAuth ready (MVP+ complete!)
7. Polish → Full feature complete

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T011)
2. Once Foundational is done:
   - Developer A: User Story 1 backend (T012-T017)
   - Developer B: User Story 4 frontend (T035-T044) - can start in parallel
   - Developer C: User Story 2 OAuth (T049-T055) - can start after US1 basics
3. User Story 3 requires Developer A to complete US1 first (T018-T032)
4. Polish phase: Team collaboration on testing (T056-T066)

---

## Manual Commands Required

**Phase 1 - Setup**:
```bash
cd backend
uv add python-jose[cryptography] passlib[bcrypt] python-multipart

cd ../frontend
npm install axios
```

**Phase 2 - Foundational (Database Migration)**:
```bash
cd backend
.venv/bin/python -m alembic revision --autogenerate -m "Add users and session_tokens tables"
.venv/bin/python -m alembic upgrade head
```

**Phase 5 - User ID Migration**:
```bash
cd backend
.venv/bin/python -m alembic revision --autogenerate -m "Add user_id to todos table"
.venv/bin/python -m alembic upgrade head
```

**Phase 9 - Testing**:
```bash
# Start backend
cd backend
.venv/bin/python -m uvicorn main:app --reload --port 8000

# Start frontend (new terminal)
cd frontend
npm run dev

# Test endpoints (curl commands from T056-T066)
```

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- User Story 5 is mostly validation - core implementation happens in User Story 3
- JWT_SECRET_KEY must be configured in environment (never access .env file)
- Google OAuth is optional (requires GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET)
- Stop at User Story 1 + 3 + 4 checkpoint for MVP validation
- Each user story should be independently completable and testable
- Database migrations must be run manually (T010-T011, T033-T034)
