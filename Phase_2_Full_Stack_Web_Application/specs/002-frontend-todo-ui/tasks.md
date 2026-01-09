# Tasks: Frontend Todo UI

**Feature**: 002-frontend-todo-ui
**Date**: 2025-12-29
**Status**: Ready for Implementation
**Generated**: via `/sp.tasks` workflow from approved plan.md, spec.md, and design artifacts

---

## Overview

This document provides a detailed, dependency-ordered task breakdown for implementing the Frontend Todo UI feature. Tasks are organized by implementation phases, with clear dependencies, acceptance criteria, and file references.

**Feature Summary**: Build a modern, responsive single-page Todo application using Next.js 14 (App Router) and ShadCN/UI components that connects to the existing FastAPI backend. Full CRUD functionality with optimistic updates, loading states, error handling, and responsive design.

**Prerequisites**:
- Backend API (feature 001-backend-todo-api) running at http://localhost:8000
- Node.js 18.17+ installed
- Git repository initialized
- Branch `002-frontend-todo-ui` created

---

## Phase 1: Setup and Infrastructure (6 tasks)

**Goal**: Initialize Next.js 14 project with ShadCN/UI and configure development environment.

**Acceptance Criteria**: Project initialized, dependencies installed, dev server runs without errors.

---

- [x] T001 Create frontend/ directory in repository root
  - **Purpose**: Establish dedicated folder for frontend code (monorepo structure)
  - **Files**: `frontend/` directory
  - **Validation**: Directory exists and is empty
  - **Notes**: Run from repository root: `mkdir -p frontend`

- [x] T002 Initialize Next.js 14 project with TypeScript and Tailwind CSS
  - **Purpose**: Bootstrap Next.js application with required configurations
  - **Files**: `frontend/package.json`, `frontend/tsconfig.json`, `frontend/tailwind.config.ts`, `frontend/next.config.js`, `frontend/app/layout.tsx`, `frontend/app/page.tsx`
  - **Command**: `cd frontend && npx create-next-app@latest . --typescript --tailwind --app --no-src-dir --import-alias "@/*"`
  - **Validation**: `npm run dev` starts server on http://localhost:3000
  - **Acceptance**: Default Next.js page loads in browser
  - **Notes**: Select Yes for TypeScript, ESLint, Tailwind, App Router; No for src/ directory

- [x] T003 Initialize ShadCN/UI with New York style and Neutral color theme
  - **Purpose**: Configure ShadCN/UI component library with project styling
  - **Files**: `frontend/components.json`, `frontend/lib/utils.ts`, updates to `frontend/app/globals.css`
  - **Command**: `npx shadcn-ui@latest init`
  - **Validation**: `components.json` exists with correct configuration
  - **Acceptance**: utils.ts has cn() function, globals.css has CSS variables
  - **Notes**: Choose New York style, Neutral color, CSS variables: Yes

- [x] T004 [P] Install required ShadCN/UI components (button, input, card)
  - **Purpose**: Add UI components for form and display elements
  - **Files**: `frontend/components/ui/button.tsx`, `frontend/components/ui/input.tsx`, `frontend/components/ui/card.tsx`
  - **Command**: `npx shadcn-ui@latest add button input card`
  - **Validation**: Component files exist in components/ui/
  - **Acceptance**: Import statements work without errors

- [x] T005 [P] Install ShadCN/UI components (checkbox, alert-dialog, toast, skeleton)
  - **Purpose**: Add components for interactions and feedback
  - **Files**: `frontend/components/ui/checkbox.tsx`, `frontend/components/ui/alert-dialog.tsx`, `frontend/components/ui/toast.tsx`, `frontend/components/ui/toaster.tsx`, `frontend/components/ui/use-toast.ts`, `frontend/components/ui/skeleton.tsx`
  - **Command**: `npx shadcn-ui@latest add checkbox alert-dialog toast skeleton`
  - **Validation**: All component files exist
  - **Acceptance**: Toast provider available, skeleton component renders

- [x] T006 Create .env.local with API base URL configuration
  - **Purpose**: Configure backend API endpoint for development
  - **Files**: `frontend/.env.local`
  - **Content**: `NEXT_PUBLIC_API_URL=http://localhost:8000`
  - **Validation**: File exists and is gitignored
  - **Acceptance**: `process.env.NEXT_PUBLIC_API_URL` resolves in code
  - **Notes**: Ensure .env.local is in .gitignore (Next.js does this by default)

---

## Phase 2: Foundational - Critical Path (2 tasks)

**Goal**: Create TypeScript types and API client that all features depend on.

**Acceptance Criteria**: Types match backend schema, API client functions are type-safe and tested.

**⚠️ BLOCKING DEPENDENCY**: ALL subsequent user story tasks depend on this phase completing first.

---

- [x] T007 Create Todo TypeScript interface in frontend/types/todo.ts
  - **Purpose**: Define type-safe data structures matching backend API
  - **Files**: `frontend/types/todo.ts`
  - **Types to Create**:
    - `Todo`: id, description, completed, created_at, updated_at
    - `CreateTodoRequest`: description
    - `UpdateTodoRequest`: description?, completed?
    - `ApiError`: detail
  - **Validation**: Types match backend models exactly (id: number, description: string, completed: boolean, timestamps: string)
  - **Acceptance**: Can import types without errors, TypeScript compiler validates structure
  - **Reference**: See api-design.md lines 36-74 for exact type definitions

- [x] T008 Implement API client with CRUD functions in frontend/lib/api.ts
  - **Purpose**: Centralize all backend communication with type-safe functions
  - **Files**: `frontend/lib/api.ts`
  - **Functions to Implement**:
    - `apiRequest<T>(endpoint, options)`: Generic HTTP wrapper with error handling
    - `fetchTodos()`: GET /api/todos → Promise<Todo[]>
    - `createTodo(description)`: POST /api/todos → Promise<Todo>
    - `updateTodo(id, updates)`: PATCH /api/todos/{id} → Promise<Todo>
    - `deleteTodo(id)`: DELETE /api/todos/{id} → Promise<void>
  - **Error Handling**: Parse error.detail from backend, handle 204 No Content, categorize errors (network/validation/not_found/server)
  - **Validation**: All functions return typed Promises, errors throw with messages
  - **Acceptance**: Can call each function from console, receives expected responses
  - **Testing**: Test with curl commands from quickstart.md (lines 555-587)
  - **Reference**: See api-design.md lines 82-230 for complete implementation

---

## Phase 3: User Story 5 - Loading & Error States (P1) (2 tasks)

**Goal**: Implement feedback mechanisms for async operations (MVP requirement).

**Acceptance Criteria**: Loading skeletons appear during fetch, toast notifications work for all operations.

**Independent Test**: Throttle network in DevTools, trigger operations, verify loading states and error messages appear correctly.

---

- [x] T009 [US5] Implement LoadingSkeleton component in frontend/components/loading-skeleton.tsx
  - **Purpose**: Display placeholder UI during initial data fetch
  - **Files**: `frontend/components/loading-skeleton.tsx`
  - **Props**: `count?: number` (default 3)
  - **Implementation**: Map count to Card components with Skeleton placeholders for checkbox and description
  - **Validation**: Component renders 3 skeleton items by default, matches TodoItem layout
  - **Acceptance**: Skeleton shows shimmer animation, has proper ARIA role="status"
  - **Reference**: See component-hierarchy.md lines 483-522, research.md lines 533-548

- [x] T010 [US5] Configure Toast notification system in frontend/app/layout.tsx
  - **Purpose**: Enable global toast notifications for success/error feedback
  - **Files**: `frontend/app/layout.tsx`, `frontend/components/ui/toast.tsx`, `frontend/components/ui/toaster.tsx`, `frontend/components/ui/use-toast.ts`
  - **Implementation**: Add `<Toaster />` component to root layout (outside main content)
  - **Validation**: Toast provider renders, useToast hook available in child components
  - **Acceptance**: Can call `toast({ title, description })` from any component
  - **Testing**: Add temporary test in page.tsx: `const { toast } = useToast(); useEffect(() => toast({ title: 'Test' }), [])`
  - **Reference**: See component-hierarchy.md lines 550-553

---

## Phase 4: User Story 1 - View and Add Todos (P1) - MVP Core (7 tasks)

**Goal**: Implement core functionality to view existing todos and create new ones.

**Acceptance Criteria**: Users can load page, see todos, add new todos via form, see success/error feedback.

**Independent Test**: Open app → see empty state → add todo "Buy groceries" → verify it appears → refresh page → verify it persists → stop backend → try to add todo → see error toast.

---

- [x] T011 [US1] Create EmptyState component in frontend/components/empty-state.tsx
  - **Purpose**: Display friendly message when no todos exist
  - **Files**: `frontend/components/empty-state.tsx`
  - **Props**: None (static content)
  - **Implementation**: Card with centered icon (CheckCircle2), heading "No todos yet", subtext "Add your first todo using the form above"
  - **Validation**: Component renders with proper styling and spacing
  - **Acceptance**: Displays correctly on mobile and desktop, muted colors, helpful message
  - **Reference**: See component-hierarchy.md lines 445-481

- [x] T012 [P] [US1] Implement TodoForm component in frontend/components/todo-form.tsx
  - **Purpose**: Input form for creating new todos with real-time validation
  - **Files**: `frontend/components/todo-form.tsx`
  - **Props**: `onSubmit: (description: string) => Promise<void>`, `isSubmitting: boolean`
  - **State**: `description` (controlled input), `error` (validation message)
  - **Validation Rules**:
    - Empty check: description.trim().length > 0
    - Max length: description.length <= 500
    - Show character counter when > 400 characters
  - **Implementation**: Form with Input (ShadCN), Button (ShadCN), error display, loading state on button
  - **Keyboard Support**: Enter to submit, clear input on success
  - **Validation**: Real-time validation on onChange, button disabled when invalid or submitting
  - **Acceptance**: Cannot submit empty description, shows error messages, button shows "Adding..." during submission
  - **Accessibility**: aria-invalid, aria-describedby for error messages
  - **Reference**: See component-hierarchy.md lines 124-218, research.md lines 393-459

- [x] T013 [P] [US1] Implement TodoItem component (view mode only) in frontend/components/todo-item.tsx
  - **Purpose**: Display individual todo with description and completion status
  - **Files**: `frontend/components/todo-item.tsx`
  - **Props**: `todo: Todo`, `onToggle: (id, completed) => Promise<void>`, `onEdit: (id, description) => Promise<void>`, `onDelete: (id) => Promise<void>`
  - **State**: `isEditing`, `editedDescription`, `isDeleting`, `showDeleteDialog` (implement minimal state for Phase 4)
  - **Phase 4 Implementation**: View mode only - Card with Checkbox (disabled for now), description text, edit button (placeholder), delete button (placeholder)
  - **Styling**: Strikethrough and muted color when completed, responsive padding (p-3 md:p-4)
  - **Validation**: Renders todo data correctly, checkbox displays checked state
  - **Acceptance**: Todos display with correct data, completed todos have visual indication
  - **Notes**: Edit and delete functionality will be added in Phases 6-7, just render placeholders for now
  - **Reference**: See component-hierarchy.md lines 264-442 (implement view mode structure only)

- [x] T014 [P] [US1] Implement TodoList component in frontend/components/todo-list.tsx
  - **Purpose**: Map todos array to TodoItem components
  - **Files**: `frontend/components/todo-list.tsx`
  - **Props**: `todos: Todo[]`, `onToggle`, `onEdit`, `onDelete` (passed through to TodoItem)
  - **Implementation**: Map todos with key={todo.id}, render TodoItem for each, space-y-3 for vertical spacing
  - **Validation**: Renders correct number of TodoItem components
  - **Acceptance**: List updates when todos array changes, proper spacing between items
  - **Accessibility**: role="list" on container
  - **Reference**: See component-hierarchy.md lines 220-262

- [x] T015 [US1] Implement app/page.tsx with state management and fetch logic
  - **Purpose**: Main application container that orchestrates all CRUD operations
  - **Files**: `frontend/app/page.tsx`
  - **State**: `todos: Todo[]`, `isLoading: boolean`, `error: string | null`
  - **Phase 4 Implementation**:
    - useEffect to fetch todos on mount (call fetchTodos from api.ts)
    - State management for todos array
    - Loading state (show LoadingSkeleton)
    - Error state (show error message with retry button)
    - Empty state (show EmptyState component)
    - Display TodoList when todos.length > 0
    - handleCreateTodo function (calls createTodo API, updates state, shows toast)
  - **Handlers**: Create handleCreateTodo (other handlers added in later phases)
  - **Layout**: Container with max-w-2xl, centered, responsive padding
  - **Validation**: Page fetches todos on load, creates new todos successfully
  - **Acceptance**: Can view todos, add new todos, see loading/error/empty states, toast notifications work
  - **Testing**: Test with backend running and offline to verify error handling
  - **Reference**: See component-hierarchy.md lines 29-119

- [x] T016 [US1] Add Toaster to layout and implement error handling helper functions
  - **Purpose**: Ensure toast notifications work globally and provide user-friendly error messages
  - **Files**: `frontend/lib/api.ts` (add error helpers), verify `frontend/app/layout.tsx` has Toaster
  - **Implementation**:
    - Add `categorizeError(error: Error): ErrorType` function
    - Add `getErrorMessage(error: Error): { title: string; description: string }` function
    - Export both functions for use in components
  - **Error Categories**: NETWORK (backend offline), VALIDATION (400), NOT_FOUND (404), SERVER (500), UNKNOWN
  - **Validation**: Can import and call getErrorMessage, returns user-friendly messages
  - **Acceptance**: Error messages are helpful and actionable (e.g., "Cannot reach server. Please check your connection.")
  - **Reference**: See api-design.md lines 239-337

- [x] T017 [US1] Test complete User Story 1 flow end-to-end
  - **Purpose**: Validate that view and add functionality works correctly
  - **Files**: Manual testing in browser
  - **Test Scenarios**:
    - ✓ Empty state displays on first load
    - ✓ Can add todo "Buy groceries" and it appears in list
    - ✓ Input clears after submission
    - ✓ Cannot submit empty description (validation error)
    - ✓ Success toast appears after adding
    - ✓ Page refresh persists todos (data comes from backend)
    - ✓ Backend offline shows error toast
    - ✓ Loading skeleton appears during initial fetch
  - **Validation**: All 8 scenarios pass
  - **Acceptance**: User Story 1 acceptance criteria met (spec.md lines 18-26)
  - **Reference**: See quickstart.md lines 278-321 for detailed test checklist

---

## Phase 5: User Story 2 - Toggle Completion (P2) (2 tasks)

**Goal**: Enable users to mark todos as complete/incomplete with optimistic updates.

**Acceptance Criteria**: Checkbox toggles completion, visual feedback immediate (<200ms), change persists, rollback on error.

**Independent Test**: Create todo → toggle checkbox → see immediate visual change → refresh page → verify status persists → stop backend → toggle → see rollback after error.

---

- [x] T018 [US2] Update TodoItem to enable checkbox with onToggle handler
  - **Purpose**: Make checkbox interactive for completion toggling
  - **Files**: `frontend/components/todo-item.tsx`
  - **Implementation**:
    - Update Checkbox component: `checked={todo.completed}`, `onCheckedChange={() => onToggle(todo.id, todo.completed)}`
    - Ensure strikethrough styling applies when completed: `className={cn('flex-1 text-sm md:text-base', todo.completed && 'line-through text-muted-foreground')}`
  - **Validation**: Checkbox is clickable, calls onToggle with correct parameters
  - **Acceptance**: Checkbox state reflects todo.completed, clickable on desktop and mobile
  - **Accessibility**: aria-label describes action (e.g., "Mark 'Buy groceries' as complete")
  - **Reference**: See component-hierarchy.md lines 297-338

- [x] T019 [US2] Implement handleToggleComplete with optimistic updates in app/page.tsx
  - **Purpose**: Toggle completion status with immediate UI feedback and rollback on error
  - **Files**: `frontend/app/page.tsx`
  - **Implementation**:
    - Snapshot todos array before mutation: `const previousTodos = [...todos]`
    - Apply optimistic update immediately: update todos state with toggled completed value
    - Call updateTodo API: `await updateTodo(id, { completed: !currentCompleted })`
    - On success: Replace optimistic update with server response, show success toast
    - On error: Restore previousTodos snapshot, show error toast with variant='destructive'
  - **Validation**: UI updates within 200ms (optimistic), rollback works when backend fails
  - **Acceptance**: Immediate visual feedback, change persists after page refresh, rollback on error
  - **Testing**: Test with backend online (success) and offline (rollback)
  - **Reference**: See research.md lines 214-281, component-hierarchy.md lines 62-80

---

## Phase 6: User Story 3 - Edit Description (P3) (2 tasks)

**Goal**: Allow users to edit todo descriptions inline with validation.

**Acceptance Criteria**: Click edit → description becomes input → can save or cancel → validation prevents empty descriptions → change persists.

**Independent Test**: Create todo "Buy milk" → click edit → change to "Buy milk and eggs" → save → verify update → refresh → verify persists.

---

- [x] T020 [US3] Add edit mode UI to TodoItem component
  - **Purpose**: Enable inline editing of todo descriptions
  - **Files**: `frontend/components/todo-item.tsx`
  - **Implementation**:
    - Add state: `isEditing`, `editedDescription`
    - View mode: Show edit button (Pencil icon) that calls `setIsEditing(true)`
    - Edit mode: Replace description with Input (value={editedDescription}, onChange updates state, autoFocus)
    - Edit mode buttons: Save (Check icon), Cancel (X icon)
    - Toggle between view/edit mode based on isEditing state
  - **Keyboard Support**: Enter key saves, Escape key cancels
  - **Validation**: Edit mode renders with input focused, buttons visible
  - **Acceptance**: Can enter edit mode, see input with current description, buttons work
  - **Reference**: See component-hierarchy.md lines 340-378

- [x] T021 [US3] Implement save and cancel handlers for edit mode
  - **Purpose**: Handle saving edited descriptions with validation and error handling
  - **Files**: `frontend/components/todo-item.tsx`
  - **Implementation**:
    - `handleSave()`: Validate trimmed description (not empty, <= 500 chars), call onEdit(todo.id, trimmed), exit edit mode on success, revert on error
    - `handleCancel()`: Reset editedDescription to todo.description, exit edit mode
    - Validation: Cannot save empty description (button disabled), shows validation error
  - **Error Handling**: On API error, revert to original description, show error toast (handled by parent)
  - **Validation**: Save button disabled when invalid, cancel reverts changes
  - **Acceptance**: Can save valid edits, cannot save empty, cancel discards changes, errors handled gracefully
  - **Testing**: Test successful edit, empty validation, backend offline error
  - **Reference**: See component-hierarchy.md lines 405-423

---

## Phase 7: User Story 4 - Delete Todo (P3) (2 tasks)

**Goal**: Allow users to delete todos with confirmation dialog.

**Acceptance Criteria**: Click delete → confirmation dialog appears → can cancel or confirm → todo removed from list on confirm.

**Independent Test**: Create todo → click delete → see dialog → cancel (todo remains) → click delete again → confirm (todo removed) → refresh (todo still gone).

---

- [x] T022 [US4] Add delete button and AlertDialog to TodoItem component
  - **Purpose**: Provide delete functionality with confirmation
  - **Files**: `frontend/components/todo-item.tsx`
  - **Implementation**:
    - Add state: `showDeleteDialog`, `isDeleting`
    - View mode: Show delete button (Trash2 icon) that calls `setShowDeleteDialog(true)`
    - Render AlertDialog: title "Delete todo?", description shows todo.description, Cancel and Delete buttons
    - Dialog state controlled by showDeleteDialog
  - **Validation**: Delete button clickable, dialog opens with correct content
  - **Acceptance**: Dialog appears on delete click, shows todo description, has cancel and confirm buttons
  - **Accessibility**: Dialog traps focus, Escape key closes dialog
  - **Reference**: See component-hierarchy.md lines 380-402

- [x] T023 [US4] Implement handleDelete function in TodoItem and app/page.tsx
  - **Purpose**: Handle todo deletion with API call
  - **Files**: `frontend/components/todo-item.tsx` (handleDelete), `frontend/app/page.tsx` (handleDeleteTodo)
  - **Implementation**:
    - TodoItem handleDelete: Set isDeleting=true, call onDelete(todo.id), close dialog, handle errors
    - app/page.tsx handleDeleteTodo: Call deleteTodo(id) API, remove from todos array, show success toast
    - Button loading state: Show "Deleting..." text during deletion
  - **Error Handling**: On error, keep todo in list, show error toast, close dialog
  - **Validation**: Todo removed from UI only after successful API response (204)
  - **Acceptance**: Todo deleted on confirm, remains on cancel, error toast if backend fails, empty state appears if last todo deleted
  - **Testing**: Test successful delete, backend offline error, delete last todo
  - **Reference**: See component-hierarchy.md lines 424-435, component-hierarchy.md lines 89-94

---

## Phase 8: Responsive Design & Polish (3 tasks)

**Goal**: Ensure application works correctly on all screen sizes and passes accessibility checks.

**Acceptance Criteria**: Application usable on 320px-1920px screens, touch targets >= 44px, keyboard navigation works.

---

- [x] T024 Test and refine mobile layout (320px - 639px)
  - **Purpose**: Verify mobile-first design works on small screens
  - **Files**: `frontend/components/*.tsx` (adjust Tailwind classes if needed)
  - **Testing**:
    - Set DevTools to iPhone SE (375px width)
    - Verify no horizontal scroll
    - Verify form stacks vertically (flex-col)
    - Verify buttons are 44px minimum (h-11 w-11)
    - Verify text readable without zoom (text-sm minimum)
    - Verify spacing between tap targets adequate
  - **Validation**: All content fits, buttons easily tappable
  - **Acceptance**: Application fully functional on mobile without zoom or horizontal scroll
  - **Reference**: See research.md lines 625-668, quickstart.md lines 499-507

- [x] T025 Test and refine tablet/desktop layout (640px - 1920px)
  - **Purpose**: Verify responsive breakpoints work correctly
  - **Files**: Review all components for responsive classes
  - **Testing**:
    - Test 768px width: Form switches to horizontal (flex-row)
    - Test 1024px width: Content centers with max-w-2xl
    - Test 1920px width: Content remains centered, not stretched
    - Verify hover states appear on desktop (hover:bg-accent)
    - Verify padding increases on larger screens (p-3 md:p-4)
  - **Validation**: Layout adapts smoothly across breakpoints
  - **Acceptance**: Application looks polished on all screen sizes, no layout issues
  - **Reference**: See research.md lines 625-668, quickstart.md lines 509-527

- [x] T026 Verify accessibility and keyboard navigation
  - **Purpose**: Ensure application meets WCAG 2.1 AA baseline
  - **Files**: All components (verify ARIA attributes)
  - **Testing**:
    - Tab through all interactive elements (proper focus order)
    - Verify focus visible styles (outline or ring)
    - Verify form errors linked with aria-describedby
    - Verify buttons have aria-label (icon buttons)
    - Verify checkbox has descriptive label
    - Test Enter key in edit mode (saves)
    - Test Escape key in edit mode (cancels)
    - Test Escape key in dialog (closes)
  - **Validation**: Can complete full workflow with keyboard only
  - **Acceptance**: All interactive elements keyboard accessible, screen reader friendly, focus indicators visible
  - **Reference**: See component-hierarchy.md lines 654-667

---

## Phase 9: Validation & Testing (2 tasks)

**Goal**: Verify all success criteria met and documentation accurate.

**Acceptance Criteria**: All 10 success criteria pass, quickstart.md instructions validated, no critical bugs.

---

- [x] T027 Run complete end-to-end workflow test
  - **Purpose**: Validate entire application workflow without errors
  - **Files**: Manual testing in browser
  - **Test Workflow**:
    1. Start with empty database
    2. Load page → verify empty state
    3. Add 3 todos → verify all appear
    4. Toggle completion on todo 1 → verify visual change
    5. Edit todo 2 description → verify update
    6. Delete todo 3 with confirmation → verify removed
    7. Refresh page → verify 2 todos persist with correct state
    8. Test on mobile (375px), tablet (768px), desktop (1920px)
    9. Stop backend → trigger operations → verify error handling
    10. Test all keyboard shortcuts (Enter, Escape, Tab)
  - **Validation**: Complete workflow executes without errors or crashes
  - **Acceptance**: All operations work, data persists, responsive design works, errors handled gracefully
  - **Reference**: See quickstart.md lines 274-567 for complete test checklist

- [x] T028 Verify all 10 success criteria from spec.md
  - **Purpose**: Confirm feature meets all defined success metrics
  - **Files**: Manual verification against spec.md lines 148-159
  - **Success Criteria to Verify**:
    - [ ] SC-001: Page load < 2 seconds (measure with Network tab)
    - [ ] SC-002: Add todo < 1 second (measure response time)
    - [ ] SC-003: Toggle optimistic update < 200ms (measure UI change)
    - [ ] SC-004: All interactive elements have hover/focus states
    - [ ] SC-005: Responsive 320px-1920px (test all breakpoints)
    - [ ] SC-006: Toast feedback within 500ms (verify timing)
    - [ ] SC-007: 100% client-side validation before submit
    - [ ] SC-008: Clear empty/loading/error states
    - [ ] SC-009: Functional when backend offline (error handling)
    - [ ] SC-010: Complete workflow without bugs
  - **Validation**: All 10 criteria met with evidence
  - **Acceptance**: Feature fully satisfies specification requirements
  - **Reference**: See plan.md lines 532-544 for success criteria mapping

---

## Dependencies & Execution Order

### Critical Path (Must Execute Sequentially)

```
Phase 1 (Setup) → Phase 2 (Foundational) → Phase 3-7 (User Stories) → Phase 8 (Polish) → Phase 9 (Validation)
```

**Blocking Dependencies**:
- **Phase 2 blocks ALL user stories**: T007-T008 must complete before T009-T028
- **User Story 1 blocks stories 2-4**: T011-T017 must complete before T018-T023
- **Phase 8-9 are final**: T024-T028 must execute last

### Within-Phase Dependencies

**Phase 1 (Setup)**:
- T001 → T002 (need directory before initialization)
- T002 → T003 (need Next.js before ShadCN)
- T003 → T004, T005 (need ShadCN init before component install)
- T004 and T005 can run in parallel ([P] markers)
- T006 independent (can run anytime in Phase 1)

**Phase 4 (User Story 1)**:
- T011, T012, T013, T014 can run in parallel ([P] markers)
- T015 depends on T011-T014 completing (needs all components)
- T016 can run in parallel with T011-T015
- T017 depends on ALL Phase 4 tasks completing

**Phases 5-7**: Sequential within phase, but each phase is independent of others (can swap order if priorities change)

---

## Parallel Opportunities

Tasks marked with [P] can execute simultaneously:

**Phase 1**:
- T004 and T005: Install different ShadCN components (no conflicts)
- T006: Create .env.local (independent of other tasks)

**Phase 2**:
- T007 and T008 have dependency: T008 imports from T007, so T007 must complete first

**Phase 4**:
- T011, T012, T013, T014: Create separate component files (no dependencies)
- T016: Add error helpers to api.ts (independent of components)

**Optimization**: A team of 2-3 developers can parallelize Phase 1 (2x speed) and Phase 4 (3x speed) by splitting [P] tasks.

---

## Implementation Strategy

### MVP-First Approach

**MVP = Phase 1 + Phase 2 + Phase 3 + Phase 4** (21 tasks: T001-T017, T009-T010)

**MVP Delivers**:
- View todos from backend
- Add new todos
- Loading skeletons during fetch
- Error handling with toast notifications
- Empty state when no todos
- Responsive design (basic)

**MVP Success**: Users can track tasks by viewing and adding todos. Provides immediate value without requiring full CRUD.

**Post-MVP**: Phases 5-7 add completion toggle (P2), edit (P3), and delete (P3) functionality incrementally.

### Incremental Delivery

Each user story phase is independently testable:
- **Phase 4 test**: View and add todos, see loading/error states
- **Phase 5 test**: Toggle completion with optimistic updates
- **Phase 6 test**: Edit descriptions inline
- **Phase 7 test**: Delete with confirmation
- **Phase 8-9 test**: Responsive design and final validation

**Benefit**: Can merge and deploy after each phase, getting user feedback early.

### Error Recovery Strategy

If a task fails:
1. Check task validation criteria (did prerequisites pass?)
2. Review reference documentation (spec.md, plan.md, design artifacts)
3. Test API endpoints manually with curl (quickstart.md lines 555-587)
4. Verify environment variables loaded (restart dev server)
5. Check browser console and terminal for errors
6. Consult troubleshooting section (quickstart.md lines 569-683)

---

## Task Count Summary

**Total Tasks**: 28

**By Phase**:
- Phase 1 (Setup): 6 tasks
- Phase 2 (Foundational): 2 tasks (BLOCKING)
- Phase 3 (US5 - Loading/Error): 2 tasks
- Phase 4 (US1 - View/Add): 7 tasks
- Phase 5 (US2 - Toggle): 2 tasks
- Phase 6 (US3 - Edit): 2 tasks
- Phase 7 (US4 - Delete): 2 tasks
- Phase 8 (Polish): 3 tasks
- Phase 9 (Validation): 2 tasks

**MVP Scope**: 21 tasks (T001-T017 + T009-T010)
**Post-MVP**: 7 tasks (T018-T028)

**Estimated Effort** (for reference, adjust based on developer experience):
- Phase 1: 1-2 hours (setup and configuration)
- Phase 2: 1-2 hours (types and API client)
- Phase 3: 1 hour (loading/error components)
- Phase 4: 3-4 hours (main UI implementation)
- Phase 5: 1-2 hours (toggle completion)
- Phase 6: 1-2 hours (edit functionality)
- Phase 7: 1-2 hours (delete functionality)
- Phase 8: 2-3 hours (responsive testing)
- Phase 9: 1-2 hours (validation)

**Total Estimated**: 12-20 hours (varies by developer experience with Next.js/React)

---

## Implementation Notes

### Code Standards (from constitution.md)

- **TypeScript Strict Mode**: All code must pass `npm run build` without errors
- **Layer Separation**: No business logic in components, all API calls via lib/api.ts
- **Component Purity**: Prefer stateless components, lift state to page.tsx when possible
- **Error Handling**: Always provide user-friendly error messages, never expose raw errors
- **Accessibility**: All interactive elements must have proper ARIA labels and keyboard support
- **Responsive Design**: Mobile-first approach, test all breakpoints

### Testing Approach

**Manual Testing Only** (per spec.md constraints):
- No automated tests in this phase
- Use quickstart.md test checklist after each phase
- Test on real devices when possible (mobile/tablet)
- Use browser DevTools for responsive testing
- Throttle network to test loading/error states

### Git Workflow

**Branching**:
```bash
git checkout -b 002-frontend-todo-ui
```

**Commit Strategy**:
- Commit after each phase completes
- Use conventional commits: `feat(ui): implement TodoForm component`
- Reference task IDs in commits: `feat(ui): add loading skeleton (T009)`

**Example Commits**:
```bash
git add .
git commit -m "feat(setup): initialize Next.js 14 with ShadCN/UI (T001-T006)"
git commit -m "feat(api): implement API client and types (T007-T008)"
git commit -m "feat(us1): implement view and add todos (T011-T017)"
```

---

## Reference Documentation

**Design Artifacts** (in `specs/002-frontend-todo-ui/`):
- `spec.md`: Feature requirements and user stories
- `plan.md`: Implementation plan and architecture decisions
- `research.md`: Technical decisions (Next.js, ShadCN/UI, API patterns)
- `component-hierarchy.md`: Component tree and state management
- `api-design.md`: API client types and functions
- `quickstart.md`: Setup instructions and test checklist

**External Resources**:
- Next.js 14 Docs: https://nextjs.org/docs
- ShadCN/UI Docs: https://ui.shadcn.com/docs
- Tailwind CSS Docs: https://tailwindcss.com/docs
- Radix UI Docs: https://www.radix-ui.com/docs/primitives/overview/introduction

---

**Tasks Document Complete**: ✅
**Ready for Implementation**: Yes
**Next Step**: Execute Phase 1 tasks (T001-T006) to initialize project

---

**Generated**: 2025-12-29 via `/sp.tasks` workflow
**Agent**: Claude Sonnet 4.5
**Template**: SDD-RI tasks.md standard format
