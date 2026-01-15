# Implementation Plan: Frontend Todo UI

**Branch**: `002-frontend-todo-ui` | **Date**: 2025-12-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-frontend-todo-ui/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a modern, responsive single-page Todo application using Next.js 14 (App Router) and ShadCN/UI components that connects to the existing FastAPI backend. The frontend will provide full CRUD functionality with optimistic updates, loading states, error handling, and responsive design from mobile to desktop. All backend communication will be centralized in lib/api.ts, and the application will follow strict layer separation principles.

## Technical Context

**Language/Version**: TypeScript 5.x (strict mode) with Next.js 14+ (App Router)
**Primary Dependencies**: Next.js 14+, React 18+, ShadCN/UI (Radix UI based), Tailwind CSS 3+, lucide-react
**Storage**: N/A (backend handles all data persistence)
**Testing**: Manual testing via browser (no automated tests in this phase)
**Target Platform**: Modern web browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
**Project Type**: Web application (frontend only - monorepo with existing backend/)
**Performance Goals**: 2s page load, 1s add response, 200ms optimistic updates
**Constraints**: No auth/multi-user, no state management libraries, no offline-first/PWA, all components must use ShadCN/UI
**Scale/Scope**: Single-page app, display all todos (no pagination), responsive 320px-1920px

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Spec-Driven Workflow (Principle I)
- ✅ Specification exists: `specs/002-frontend-todo-ui/spec.md` (validated, all checks passed)
- ✅ Planning phase active (this document)
- ⏳ Tasks phase pending (after plan completion)
- ⏳ Implementation pending (after tasks breakdown)

### ✅ Layer Separation (Principle II)
- ✅ Frontend isolated in dedicated `frontend/` folder
- ✅ All backend communication centralized in `lib/api.ts` (no scattered fetch calls)
- ✅ No direct database access from frontend
- ✅ No business logic in components (delegates to backend)
- ✅ Components focused on UI only
- ✅ Pages focused on layout and composition only

### ✅ Frontend Architecture (Principle IV)
- ✅ Component-based architecture with reusable UI elements
- ✅ Centralized API client pattern enforced
- ✅ Single-purpose components planned
- ✅ Clear separation: components/ for reusables, app/ for pages, lib/ for API

### ✅ Monorepo Structure (Principle VII)
- ✅ Frontend code in dedicated `frontend/` folder
- ✅ Existing backend code in `backend/` folder (feature 001)
- ✅ No mixing of layers
- ✅ Shared types only if truly cross-layer (planned in frontend/src/types/)

### ⚠️ Task Definition Standard (Principle VIII)
- ✅ Spec completed and validated
- ✅ Plan in progress (this document)
- ⏳ Tasks will be generated after plan completion via `/sp.tasks`
- ⏳ Tasks will include: ID, purpose, files, acceptance criteria, boundaries, validation

**Gate Status**: ✅ PASSED - All applicable principles satisfied. Proceed to Phase 0.

**Re-evaluation Checkpoint**: After Phase 1 design artifacts are complete, re-verify that component hierarchy, API client design, and folder structure maintain layer separation and architectural boundaries.

## Project Structure

### Documentation (this feature)

```text
specs/002-frontend-todo-ui/
├── spec.md              # Feature specification (/sp.specify command - COMPLETE)
├── checklists/
│   └── requirements.md  # Validation checklist (COMPLETE - 14/14 passed)
├── plan.md              # This file (/sp.plan command - IN PROGRESS)
├── research.md          # Phase 0 output (/sp.plan command - PENDING)
├── component-hierarchy.md  # Phase 1 output (/sp.plan command - PENDING)
├── api-design.md        # Phase 1 output (/sp.plan command - PENDING)
├── quickstart.md        # Phase 1 output (/sp.plan command - PENDING)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Monorepo structure (web application)

backend/                 # Existing FastAPI backend (feature 001-backend-todo-api)
├── main.py
├── routes/
│   └── todos.py
├── services/
│   └── todo_service.py
├── models/
│   └── todo.py
└── core/
    └── config.py

frontend/                # New Next.js 14 frontend (feature 002-frontend-todo-ui)
├── src/
│   ├── app/            # Next.js App Router pages
│   │   ├── page.tsx    # Root route (main todo page)
│   │   └── layout.tsx  # Root layout
│   ├── components/     # Reusable UI components
│   │   ├── todo-list.tsx
│   │   ├── todo-item.tsx
│   │   ├── todo-form.tsx
│   │   ├── empty-state.tsx
│   │   ├── loading-skeleton.tsx
│   │   └── ui/         # ShadCN/UI components (auto-generated)
│   ├── lib/
│   │   └── api.ts      # Centralized API client (ONLY place for backend calls)
│   └── types/
│       └── todo.ts     # TypeScript interfaces matching backend
├── public/
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.js
└── components.json     # ShadCN/UI configuration
```

**Structure Decision**: Web application monorepo structure selected. Frontend isolated in `frontend/` folder to maintain layer separation (Constitution Principle II). Backend already exists in `backend/` folder from feature 001. This structure enables independent development, testing, and deployment of frontend and backend while maintaining clear architectural boundaries.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. All architectural principles satisfied.

---

## Phase 0: Research & Technical Decisions

**Purpose**: Resolve technical unknowns and establish implementation patterns before design.

### Research Tasks

**R1: Next.js 14 App Router Setup**
- Decision needed: Project initialization approach (create-next-app vs manual setup)
- Decision needed: TypeScript configuration (strict mode settings)
- Decision needed: Tailwind CSS integration pattern
- Outcome: Document exact initialization commands and configuration files

**R2: ShadCN/UI Integration**
- Decision needed: Component installation strategy (individual vs bulk)
- Decision needed: Which components needed: Button, Input, Card, Dialog, Toast, Skeleton
- Decision needed: Custom theme configuration requirements
- Outcome: Document `npx shadcn-ui@latest add <component>` workflow

**R3: API Client Architecture**
- Decision needed: Native fetch vs library (axios, ky, etc.)
- Decision needed: Error handling pattern for 4xx/5xx responses
- Decision needed: Request/response type safety approach
- Outcome: Document API client structure with TypeScript generics

**R4: Optimistic Update Pattern**
- Decision needed: State snapshot approach before mutation
- Decision needed: Rollback mechanism on error
- Decision needed: UI feedback during optimistic period
- Outcome: Document pattern with try/catch and state restoration

**R5: Error Handling Strategy**
- Decision needed: Toast notification library (ShadCN Toast vs react-hot-toast)
- Decision needed: Error message format and presentation
- Decision needed: Network error vs validation error differentiation
- Outcome: Document error handling flow with toast notifications

**R6: Form Validation**
- Decision needed: Client-side validation approach (controlled inputs vs validation library)
- Decision needed: Validation trigger timing (onChange vs onSubmit)
- Decision needed: Error display pattern
- Outcome: Document validation pattern with real-time feedback

**R7: Loading State Management**
- Decision needed: Skeleton loader design (content-based vs generic)
- Decision needed: Loading indicator for mutations (button disabled vs spinner)
- Decision needed: Global loading state vs component-level
- Outcome: Document loading patterns with ShadCN Skeleton component

**R8: Responsive Design Approach**
- Decision needed: Breakpoint strategy (Tailwind defaults vs custom)
- Decision needed: Mobile-first vs desktop-first approach
- Decision needed: Touch target sizes for mobile interactions
- Outcome: Document responsive patterns with Tailwind utility classes

**Output**: `specs/002-frontend-todo-ui/research.md` with all decisions documented in format:
```markdown
### R#: Decision Title
**Decision**: [What was chosen]
**Rationale**: [Why chosen]
**Alternatives Considered**: [What else was evaluated]
**Implementation Notes**: [How to implement]
```

---

## Phase 1: Design & Contracts

**Prerequisites**: `research.md` complete (all NEEDS CLARIFICATION resolved)

### D1: Component Hierarchy Design

**Purpose**: Define component tree, responsibilities, and props interfaces.

**Output**: `specs/002-frontend-todo-ui/component-hierarchy.md`

**Content Structure**:
```markdown
# Component Hierarchy

## Page Components
### app/page.tsx (Root Page)
- Purpose: Main todo page container
- State: todos[], isLoading, error
- Children: TodoForm, TodoList, EmptyState, LoadingSkeleton
- Responsibilities: Fetch todos on mount, manage global state, coordinate mutations

## Feature Components
### TodoForm
- Purpose: Add new todo input form
- Props: onSubmit(description), isSubmitting
- State: description (controlled input)
- Responsibilities: Input validation, form submission, loading state

### TodoList
- Purpose: Display list of todos
- Props: todos[], onToggle(id), onEdit(id, description), onDelete(id)
- Children: TodoItem (multiple)
- Responsibilities: Map todos to TodoItem components

### TodoItem
- Purpose: Single todo display with actions
- Props: todo, onToggle, onEdit, onDelete, isUpdating
- State: isEditing, editedDescription
- Responsibilities: Display todo, handle inline editing, trigger mutations

### EmptyState
- Purpose: Display message when no todos exist
- Props: none
- Responsibilities: Show helpful message and illustration

### LoadingSkeleton
- Purpose: Display skeleton loaders during fetch
- Props: count (number of skeleton items)
- Responsibilities: Render placeholder UI

## ShadCN/UI Components (from ui/)
- Button: Form submit, edit, delete actions
- Input: Todo description field
- Card: Todo item container
- Checkbox: Completion toggle
- Dialog: Delete confirmation
- Toast: Success/error notifications
- Skeleton: Loading placeholders
```

### D2: API Client Design

**Purpose**: Define API client functions, types, and error handling.

**Output**: `specs/002-frontend-todo-ui/api-design.md`

**Content Structure**:
```markdown
# API Client Design

## Configuration
- Base URL: http://localhost:8000/api/todos
- Headers: Content-Type: application/json
- Error handling: Parse error.detail from backend responses

## Type Definitions (types/todo.ts)
```typescript
export interface Todo {
  id: number;
  description: string;
  completed: boolean;
  created_at: string; // ISO 8601
  updated_at: string; // ISO 8601
}

export interface CreateTodoRequest {
  description: string;
}

export interface UpdateTodoRequest {
  description?: string;
  completed?: boolean;
}

export interface ApiError {
  detail: string;
}
```

## API Functions (lib/api.ts)

### fetchTodos(): Promise<Todo[]>
- Method: GET /api/todos
- Returns: Array of todos
- Throws: Error with message on network/server error

### createTodo(description: string): Promise<Todo>
- Method: POST /api/todos
- Body: { description }
- Returns: Created todo (201)
- Throws: Error on validation (400) or server error

### updateTodo(id: number, updates: UpdateTodoRequest): Promise<Todo>
- Method: PATCH /api/todos/{id}
- Body: { description?, completed? }
- Returns: Updated todo (200)
- Throws: Error on 404 or validation error

### deleteTodo(id: number): Promise<void>
- Method: DELETE /api/todos/{id}
- Returns: void (204)
- Throws: Error on 404 or server error

## Error Handling Pattern
```typescript
async function apiRequest<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...options?.headers }
  });

  if (!response.ok) {
    const error: ApiError = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.status === 204 ? undefined as T : await response.json();
}
```
```

### D3: Quickstart Guide

**Purpose**: Document setup, running, and testing instructions.

**Output**: `specs/002-frontend-todo-ui/quickstart.md`

**Content Structure**:
```markdown
# Frontend Todo UI - Quickstart Guide

## Prerequisites
- Node.js 18+ and npm/yarn/pnpm
- Backend API running at http://localhost:8000 (see specs/001-backend-todo-api/quickstart.md)

## Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Initialize Next.js 14 project:
   ```bash
   npx create-next-app@latest . --typescript --tailwind --app --no-src-dir
   ```

3. Install ShadCN/UI:
   ```bash
   npx shadcn-ui@latest init
   ```
   - Choose: New York style, Neutral color, CSS variables

4. Add required components:
   ```bash
   npx shadcn-ui@latest add button input card checkbox dialog toast skeleton
   ```

5. Install dependencies:
   ```bash
   npm install
   ```

## Running

1. Start backend (in separate terminal):
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. Start frontend:
   ```bash
   cd frontend
   npm run dev
   ```

3. Open browser:
   ```
   http://localhost:3000
   ```

## Manual Testing Checklist

### User Story 1: View and Add Todos (P1)
- [ ] Empty state displays when no todos exist
- [ ] Can type in input field and click "Add" button
- [ ] New todo appears in list immediately
- [ ] Input clears after submission
- [ ] Cannot submit empty description (validation error shows)
- [ ] Success toast appears after adding todo
- [ ] Error toast appears if backend is offline

### User Story 2: Toggle Completion (P2)
- [ ] Can click checkbox to mark todo complete
- [ ] Visual indication appears (strikethrough or style change)
- [ ] Can click again to mark incomplete
- [ ] Change persists after page refresh
- [ ] Optimistic update occurs immediately
- [ ] Rollback happens if backend fails

### User Story 3: Edit Description (P3)
- [ ] Can click edit button to enable editing
- [ ] Description becomes editable input
- [ ] Can save changes
- [ ] Can cancel without saving
- [ ] Cannot save empty description

### User Story 4: Delete Todo (P3)
- [ ] Can click delete button
- [ ] Confirmation dialog appears
- [ ] Can cancel deletion
- [ ] Can confirm deletion
- [ ] Todo removed from list

### User Story 5: Loading and Error States (P1)
- [ ] Skeleton loaders appear during initial fetch
- [ ] Submit button shows loading state during creation
- [ ] Error messages clear and helpful
- [ ] Network errors handled gracefully

### Responsive Design
- [ ] Test on 320px width (mobile)
- [ ] Test on 768px width (tablet)
- [ ] Test on 1920px width (desktop)
- [ ] Touch targets large enough on mobile

## Troubleshooting

**Backend Connection Error**:
- Verify backend is running: `curl http://localhost:8000/health`
- Check CORS configuration in backend

**ShadCN Components Not Found**:
- Re-run: `npx shadcn-ui@latest add <component>`
- Check `components.json` configuration

**TypeScript Errors**:
- Ensure strict mode is enabled in tsconfig.json
- Run: `npm run build` to check for errors
```

### D4: Update Agent Context

**Purpose**: Register new frontend technology in agent-specific context file.

**Action**: Run `.specify/scripts/bash/update-agent-context.sh claude`

**Expected Update**: Add to appropriate agent context:
```markdown
## Technology Stack (Updated)
- Frontend: Next.js 14 (App Router), TypeScript, ShadCN/UI, Tailwind CSS
- Backend: FastAPI, Python 3.11+, Pydantic
```

---

## Phase 2: Implementation Phases (Overview)

**Note**: Detailed task breakdown will be generated by `/sp.tasks` command. This section provides high-level phase structure for reference.

### Phase A: Project Setup
- Initialize Next.js 14 project in `frontend/` folder
- Configure TypeScript, Tailwind CSS
- Install and configure ShadCN/UI
- Create folder structure: app/, components/, lib/, types/

### Phase B: Foundational (Blocking Prerequisites)
- Create TypeScript types (types/todo.ts) matching backend
- Implement API client (lib/api.ts) with all CRUD functions
- Add error handling and type safety

### Phase C: User Story 5 - Loading & Error States (P1)
- Implement LoadingSkeleton component
- Implement toast notification system
- Create error handling patterns

### Phase D: User Story 1 - View and Add Todos (P1) 🎯 MVP
- Implement app/page.tsx with state management
- Implement TodoForm component
- Implement TodoList and TodoItem components (display only)
- Implement EmptyState component
- Test: Create and view todos

### Phase E: User Story 2 - Toggle Completion (P2)
- Add checkbox to TodoItem
- Implement optimistic update pattern
- Handle completion toggle with rollback
- Test: Toggle completion status

### Phase F: User Story 3 - Edit Description (P3)
- Add edit mode to TodoItem
- Implement inline editing with save/cancel
- Add validation for empty descriptions
- Test: Edit and save descriptions

### Phase G: User Story 4 - Delete Todo (P3)
- Implement delete confirmation Dialog
- Add delete handler with API call
- Test: Delete with confirmation

### Phase H: Responsive Design & Polish
- Add responsive breakpoints with Tailwind
- Test on mobile, tablet, desktop
- Refine touch targets and spacing
- Verify accessibility (focus states, keyboard navigation)

### Phase I: Validation & Documentation
- Run complete end-to-end workflow test
- Verify all 10 success criteria met
- Validate quickstart.md instructions
- Update README if needed

---

## Success Criteria Mapping

All 10 success criteria from spec.md will be verified during implementation:

- **SC-001**: Page load < 2 seconds → Measure in Phase D
- **SC-002**: Add todo < 1 second → Measure in Phase D
- **SC-003**: Optimistic update < 200ms → Measure in Phase E
- **SC-004**: Visual states for interactive elements → Verify in Phase H
- **SC-005**: Responsive 320px-1920px → Test in Phase H
- **SC-006**: Feedback within 500ms → Verify in Phase C
- **SC-007**: 100% client validation → Implement in Phases D, F
- **SC-008**: Clear empty/loading/error states → Verify in Phases C, D
- **SC-009**: Functional when offline → Test in Phase I
- **SC-010**: Complete workflow without bugs → Test in Phase I

---

## Risk Analysis

### Technical Risks

**Risk 1: CORS Issues Between Frontend and Backend**
- **Probability**: Medium
- **Impact**: High (blocks all API calls)
- **Mitigation**: Document CORS configuration in backend, test with curl first, add CORS middleware if needed
- **Contingency**: Use Next.js API routes as proxy if CORS cannot be resolved

**Risk 2: ShadCN/UI Component Installation Failures**
- **Probability**: Low
- **Impact**: Medium (delays component implementation)
- **Mitigation**: Follow exact initialization steps, verify Node.js version compatibility
- **Contingency**: Manually copy component code from ShadCN documentation

**Risk 3: Optimistic Update Race Conditions**
- **Probability**: Medium
- **Impact**: Medium (inconsistent UI state)
- **Mitigation**: Implement proper rollback mechanism, use request IDs to track inflight requests
- **Contingency**: Fall back to non-optimistic updates if race conditions persist

### Architectural Risks

**Risk 4: State Management Complexity Without Library**
- **Probability**: Low
- **Impact**: Medium (maintenance burden)
- **Mitigation**: Keep state simple with React useState, centralize in page.tsx, document patterns clearly
- **Contingency**: If complexity grows, create ADR and propose Zustand/Redux integration

**Risk 5: Mobile Touch Interaction Issues**
- **Probability**: Low
- **Impact**: Medium (poor mobile UX)
- **Mitigation**: Follow touch target size guidelines (44x44px minimum), test on real devices
- **Contingency**: Adjust component sizing, add spacing, implement swipe gestures

---

## Next Steps

1. **Complete Phase 0**: Generate `research.md` by researching all 8 technical decisions (R1-R8)
2. **Complete Phase 1**: Generate design artifacts (component-hierarchy.md, api-design.md, quickstart.md)
3. **Update Agent Context**: Run update-agent-context.sh to register frontend technology
4. **Re-evaluate Constitution**: Verify layer separation maintained in design
5. **Generate Tasks**: Run `/sp.tasks` to create detailed task breakdown from this plan
6. **Create PHR**: Document planning process in Prompt History Record

---

## Architectural Decision Records (Pending)

After implementation planning, consider creating ADRs for significant decisions:

**Potential ADR 1**: "Use Native Fetch Instead of Axios for API Client"
- **Why**: Reduces bundle size, modern browser support, sufficient for CRUD operations
- **Significance**: Affects error handling patterns and request interceptor approach
- **Status**: Pending user consent - suggest after research phase

**Potential ADR 2**: "No Global State Management Library"
- **Why**: Simple CRUD operations don't justify Redux/Zustand complexity
- **Significance**: Affects maintainability and scalability long-term
- **Status**: Pending user consent - suggest after task breakdown

---

**Plan Status**: ✅ COMPLETE - Ready for Phase 0 (Research)
**Next Command**: Continue with `/sp.plan` workflow to generate research.md
