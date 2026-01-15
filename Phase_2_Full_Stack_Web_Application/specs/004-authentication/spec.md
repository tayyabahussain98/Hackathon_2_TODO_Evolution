# Feature Specification: Better Auth with JWT and OAuth Support

**Feature Branch**: `004-authentication`
**Created**: 2025-12-30
**Status**: Draft
**Input**: User description: "Add Better Auth to full-stack todo app with JWT tokens for sessions, Google OAuth for login/signup, protected routes in FastAPI, protected pages in frontend, and user-specific todos"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Email/Password Authentication (Priority: P1)

Users can create an account with email and password, log in with email/password, and access protected todo endpoints. The system validates credentials, issues JWT tokens for session management, and ensures passwords are securely stored using bcrypt hashing.

**Why this priority**: This is the core authentication mechanism. Without email/password auth, users cannot create accounts or access the system. It provides a fallback when OAuth is not available and enables immediate user onboarding.

**Independent Test**: Can be fully tested by creating an account, logging in, receiving a JWT token, and accessing protected endpoints with the token. Delivers the fundamental value of secure access control.

**Acceptance Scenarios**:

1. **Given** the system is operational, **When** a user visits the signup page and enters a valid email and password, **Then** the user account is created, passwords are hashed, and a JWT token is returned
2. **Given** a user account exists, **When** the user logs in with correct email/password, **Then** the system validates credentials and returns a JWT token
3. **Given** a user attempts to log in with incorrect credentials, **When** the system validates and returns a 401 Unauthorized error
4. **Given** a user logs in successfully, **When** the user receives a JWT token that can be used to access protected endpoints
5. **Given** a user has a valid JWT token, **When** the user accesses a protected endpoint, **Then** the system validates the token and grants access

---

### User Story 2 - Google OAuth Authentication (Priority: P2)

Users can sign up and log in using their Google account. The system uses Better Auth's OAuth provider to authenticate users, creates or links existing accounts, and issues JWT tokens for session management.

**Why this priority**: Google OAuth provides a convenient, secure login method that most users prefer. It eliminates password management and improves security by leveraging Google's authentication infrastructure. This is an enhancement to the core email/password auth.

**Independent Test**: Can be fully tested by initiating a Google OAuth flow, completing authentication, receiving a JWT token, and accessing protected endpoints with the token. Delivers value of seamless third-party authentication.

**Acceptance Scenarios**:

1. **Given** the system is operational, **When** a user clicks "Sign up with Google", **Then** the system redirects to Google's OAuth consent page
2. **Given** Google's consent page, **When** the user authorizes the application, **Then** Google redirects back to the application with an authorization code
3. **Given** the application receives an authorization code, **When** the application exchanges it with Better Auth for a JWT token and creates/links a user account
4. **Given** a user has previously signed up with Google, **When** they click "Log in with Google", **Then** the system authenticates them via OAuth and returns a JWT token
5. **Given** a user has a JWT token from OAuth, **When** they access protected endpoints, **Then** the system validates the token and grants access
6. **Given** a user account exists with email/password, **When** they sign up with Google, **Then** the system links the Google account to their existing email/password account

---

### User Story 3 - Protected API Routes (Priority: P1)

Only authenticated users can access protected API endpoints. The system validates JWT tokens in the Authorization header for each request and returns 401 Unauthorized for invalid or expired tokens. Each user can only CRUD their own todos.

**Why this priority**: This is essential for data security and privacy. Without protected routes, all todos are globally accessible, which violates the requirement for user-specific todos. This must be implemented before or alongside user story 4.

**Independent Test**: Can be fully tested by creating two user accounts, generating JWT tokens for each, and attempting to access User A's todos with User B's token. Delivers the fundamental value of multi-tenant data isolation.

**Acceptance Scenarios**:

1. **Given** a user has a valid JWT token, **When** they POST to /api/todos, **Then** the todo is created with their user_id and persisted in the database
2. **Given** a user has a valid JWT token, **When** they GET /api/todos, **Then** the system returns only todos belonging to that user
3. **Given** a user attempts to access /api/todos without a token, **Then** the system returns 401 Unauthorized
4. **Given** a user attempts to access /api/todos with an invalid token, **Then** the system returns 401 Unauthorized
5. **Given** User A has a valid token, **When** they attempt to GET /api/todos/5 (User B's todo), **Then** the system returns 403 Forbidden
6. **Given** a user has a valid token, **When** they PATCH /api/todos/1 (their todo), **Then** the todo is updated successfully
7. **Given** a user has a valid token, **When** they DELETE /api/todos/1 (their todo), **Then** the todo is deleted successfully
8. **Given** a user has a valid token, **When** they attempt to access /api/todos/123 (non-existent todo), **Then** the system returns 404 Not Found

---

### User Story 4 - Protected Frontend Pages (Priority: P1)

Only authenticated users can view and interact with the todo application pages. Unauthenticated users are redirected to the login page. The frontend manages JWT tokens in localStorage and includes them in Authorization headers for API requests.

**Why this priority**: This completes the user experience by enforcing authentication on the frontend. Without protected pages, users could bypass the frontend login and directly call the API. This must be implemented alongside user story 3.

**Independent Test**: Can be fully tested by accessing the application without a token (redirects to login), logging in (receives token), and accessing protected pages (accessible). Delivers the complete end-to-end user journey.

**Acceptance Scenarios**:

1. **Given** a user is not authenticated, **When** they visit the todo application homepage, **Then** they are redirected to the login page
2. **Given** a user is not authenticated, **When** they attempt to directly access a protected page URL, **Then** they are redirected to the login page
3. **Given** a user is not authenticated, **When** they attempt to call an API endpoint from the browser console, **Then** the API returns 401 Unauthorized
4. **Given** a user visits the login page, **When** they successfully authenticate, **Then** they are redirected to the homepage
5. **Given** a user is authenticated, **When** they visit the homepage, **Then** they can view their todos
6. **Given** a user is authenticated, **When** their JWT token expires, **Then** the system redirects them to the login page automatically
7. **Given** a user is authenticated, **When** they log out, **Then** their token is cleared and they are redirected to the login page

---

### User Story 5 - User-Specific Todos (Priority: P1)

Each user can only access their own todos. The database schema is updated to include a user_id foreign key, and all CRUD operations filter by the authenticated user's ID.

**Why this priority**: This is the core data isolation requirement specified in the original request. Without user-scoped todos, the system would not provide true multi-tenancy. This must be implemented after the database integration and authentication are in place.

**Independent Test**: Can be fully tested by creating two user accounts, logging in as each user, creating todos, and verifying that each user can only see their own todos. Delivers the fundamental value of data privacy and multi-tenancy.

**Acceptance Scenarios**:

1. **Given** a user is authenticated, **When** they create a todo, **Then** the todo is saved with their user_id
2. **Given** two users are authenticated, **When** User A creates a todo, **Then** User B cannot see or access User A's todo
3. **Given** two users are authenticated, **When** User A and User B both list todos, **Then** each user sees only their own todos
4. **Given** two users are authenticated, **When** User A updates their todo, **Then** User B's view is unaffected
5. **Given** two users are authenticated, **When** User A deletes their todo, **Then** User B's view is unaffected
6. **Given** two users are authenticated, **When** User A attempts to access User B's todo by ID, **Then** the system returns 403 Forbidden

---

### Edge Cases

- What happens when a user forgets their password?
- How does the system handle concurrent login attempts with the same credentials?
- What happens when a user's JWT token expires mid-request?
- What happens when Better Auth service is temporarily unavailable?
- How does the system handle OAuth authorization code expiration?
- What happens when a user tries to link an OAuth account to an email account with a different email than the OAuth email?
- How does the system handle CSRF attacks on OAuth flow?
- What happens when the database connection fails during user creation?

## Requirements *(mandatory)*

### Functional Requirements

**FR-001**: System MUST support user account creation with email and password
**FR-002**: System MUST validate email format during account creation
**FR-003**: System MUST enforce password complexity requirements (minimum 8 characters)
**FR-004**: System MUST hash passwords using bcrypt with a minimum work factor of 12
**FR-005**: System MUST allow users to log in with email and password
**FR-006**: System MUST validate credentials and return appropriate error messages for incorrect email or password
**FR-007**: System MUST issue JWT tokens with 24-hour expiration time
**FR-008**: System MUST use Better Auth's Email & Password provider
**FR-009**: System MUST use Better Auth's Google OAuth provider
**FR-010**: System MUST handle OAuth redirect URLs for development and production environments
**FR-011**: System MUST create or link user accounts when OAuth authentication completes
**FR-012**: System MUST validate JWT tokens on each protected API request
**FR-013**: System MUST return 401 Unauthorized for missing, invalid, or expired tokens
**FR-014**: System MUST extract user_id from JWT token for database queries
**FR-015**: System MUST add user_id foreign key to todos table
**FR-016**: System MUST filter all todo queries by authenticated user_id
**FR-017**: System MUST return 403 Forbidden when users attempt to access todos they don't own
**FR-018**: System MUST protect all todo API endpoints (POST, GET, PATCH, DELETE)
**FR-019**: System MUST provide login page in frontend
**FR-020**: System MUST provide signup page in frontend
**FR-021**: System MUST store JWT token in localStorage after successful authentication
**FR-022**: System MUST include JWT token in Authorization header for all API requests
**FR-023**: System MUST redirect unauthenticated frontend users to login page
**FR-024**: System MUST provide logout functionality that clears JWT token
**FR-025**: System MUST redirect users to login page on token expiration
**FR-026**: System MUST handle OAuth state parameter for CSRF protection
**FR-027**: System MUST handle OAuth error responses gracefully
**FR-028**: System MUST allow password reset functionality (send reset email, validate reset token)
**FR-029**: System MUST complete all operations within 2 seconds under normal load (100 concurrent users)
**FR-030**: System MUST handle Better Auth service outages gracefully with appropriate error messages

### Key Entities *(include if feature involves data)*

- **User**: Represents an application user with authentication credentials and profile
  - Attributes:
    - id: Unique identifier (UUID or auto-increment)
    - email: Unique email address (required, indexed, max 255 characters)
    - password_hash: Hashed password using bcrypt (required)
    - created_at: Account creation timestamp
    - updated_at: Account modification timestamp
    - google_id: Optional Google account identifier (for OAuth linking)

- **SessionToken**: Represents a JWT session token issued to users
  - Attributes:
    - id: Unique identifier
    - user_id: Foreign key to User
    - token: JWT token string
    - expires_at: Token expiration timestamp
    - created_at: Token issuance timestamp

- **Todo**: Represents a task or item to be tracked (existing table, modified to add user_id)
  - Attributes (existing):
    - id: Primary key, auto-incrementing
    - description: Task description (required, max 500 characters)
    - completed: Boolean (default False)
    - created_at: Creation timestamp
    - updated_at: Last modification timestamp
  - Attributes (new):
    - user_id: Foreign key to User table (required, indexed)
    - owner of the todo

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of users can successfully create accounts with valid email and password
- **SC-002**: 100% of valid login attempts succeed within 2 seconds
- **SC-003**: 100% of invalid login attempts return 401 Unauthorized
- **SC-004**: 100% of Google OAuth flows complete successfully when users authorize
- **SC-005**: 100% of protected API endpoints reject requests without valid tokens with 401 Unauthorized
- **SC-006**: 100% of protected API endpoints reject requests with other user's tokens with 403 Forbidden
- **SC-007**: 100% of users can only CRUD their own todos (data isolation verified)
- **SC-008**: All frontend pages redirect unauthenticated users to login page
- **SC-009**: 100% of authenticated users can access protected pages
- **SC-010**: 100% of JWT tokens expire after 24 hours and users are automatically redirected to login
- **SC-011**: System handles at least 1000 concurrent users without API degradation
- **SC-012**: Password reset functionality works end-to-end (email sent, token validated, password updated)
- **SC-013**: Better Auth service outages result in appropriate error messages (not crashes)
- **SC-014**: OAuth account linking works correctly (links to existing email account, creates new account if no match)

## Out of Scope

The following are explicitly excluded from this feature:

- Two-factor authentication (2FA) - beyond initial implementation
- Email verification for account creation - can be added later
- Password history tracking - passwords can be reset without tracking
- Account deactivation and soft delete - accounts remain active
- Admin/role-based access control - all users have equal permissions
- Social login providers beyond Google (Facebook, GitHub, etc.)
- User profile management beyond email and OAuth linking
- Push notifications for authentication events
- Session management beyond JWT (no refresh tokens, no device tracking)
- Audit logging beyond basic security events
- Rate limiting on login attempts - can be added later
- IP-based access restrictions - can be added later
- Advanced OAuth features (offline access, incremental authorization)
- Database migrations beyond user schema changes - only schema modifications needed

## Assumptions

- Better Auth is properly configured with valid Better Auth secret key
- Better Auth Email & Password provider is enabled in the project
- Better Auth Google OAuth provider is enabled in the project
- Frontend can store and retrieve JWT tokens from localStorage
- Frontend can include Authorization headers in API requests
- PostgreSQL database is accessible for schema migrations
- Users have valid email addresses (email validation is sufficient)
- Users are using modern browsers with localStorage support
- Network connectivity to Better Auth is stable
- OAuth redirect URLs are properly configured in Better Auth dashboard

## Dependencies

- Existing backend: FastAPI with PostgreSQL database
- Existing frontend: Next.js 14+ with ShadCN/UI components
- Better Auth SDK for Python (better-auth/python package)
- Better Auth SDK for JavaScript (better-auth/react package)
- bcrypt password hashing library for Python
- PyJWT for token generation
- Alembic for database migrations

## Constraints

- Must NEVER access, read, display, or mention the contents of any .env file
- Better Auth secret key is provided via environment variable (BETTER_AUTH_SECRET)
- OAuth redirect URLs must be properly configured for development and production
- Passwords must be hashed with bcrypt before storage (no plaintext passwords stored)
- JWT tokens must be signed with secret key and validated on each protected request
- User isolation must be enforced at both API and database levels
- Must maintain backward compatibility with existing todo API endpoints (add user_id, don't remove existing functionality)
- Must use type hints throughout the codebase
- Frontend must handle authentication errors gracefully with user-friendly messages
