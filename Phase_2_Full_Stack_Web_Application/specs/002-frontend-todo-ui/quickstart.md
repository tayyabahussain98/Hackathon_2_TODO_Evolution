# Frontend Todo UI - Quickstart Guide

**Feature**: 002-frontend-todo-ui
**Date**: 2025-12-29
**Purpose**: Complete setup, running, and manual testing instructions for Next.js 14 + ShadCN/UI frontend

---

## Prerequisites

### Required Software
- **Node.js**: Version 18.17+ or 20+ (LTS recommended)
- **Package Manager**: npm (comes with Node.js) or yarn or pnpm
- **Git**: For version control and branching
- **Code Editor**: VS Code recommended (with TypeScript/ESLint extensions)

### Verify Installation
```bash
# Check Node.js version
node --version
# Expected: v18.17.0 or higher

# Check npm version
npm --version
# Expected: v9.0.0 or higher
```

### Backend Dependency
- **Backend API**: Must be running at http://localhost:8000
- **Reference**: See `specs/001-backend-todo-api/quickstart.md` for backend setup
- **Health Check**: `curl http://localhost:8000/health` should return `{"status":"healthy"}`

---

## Setup Instructions

### Step 1: Initialize Next.js 14 Project

Navigate to the repository root and create the frontend directory:

```bash
# From repository root
mkdir -p frontend
cd frontend
```

Initialize Next.js 14 with TypeScript and Tailwind CSS:

```bash
npx create-next-app@latest . --typescript --tailwind --app --no-src-dir --import-alias "@/*"
```

**Configuration Prompts** (if asked):
- ✅ Would you like to use TypeScript? → **Yes**
- ✅ Would you like to use ESLint? → **Yes**
- ✅ Would you like to use Tailwind CSS? → **Yes**
- ✅ Would you like to use `src/` directory? → **No**
- ✅ Would you like to use App Router? → **Yes**
- ✅ Would you like to customize the default import alias? → **No** (use `@/*`)

**Files Created**:
- `package.json` - Project dependencies
- `tsconfig.json` - TypeScript configuration
- `tailwind.config.ts` - Tailwind CSS configuration
- `next.config.js` - Next.js configuration
- `app/layout.tsx` - Root layout
- `app/page.tsx` - Home page (will be replaced)
- `.eslintrc.json` - ESLint configuration

### Step 2: Install ShadCN/UI

Initialize ShadCN/UI in the project:

```bash
npx shadcn-ui@latest init
```

**Configuration Prompts**:
- Which style would you like to use? → **New York**
- Which color would you like to use as base color? → **Neutral**
- Where is your global CSS file? → **app/globals.css** (default)
- Would you like to use CSS variables for colors? → **Yes**
- Where is your tailwind.config.js located? → **tailwind.config.ts** (default)
- Configure the import alias for components: → **@/components** (default)
- Configure the import alias for utils: → **@/lib/utils** (default)
- Are you using React Server Components? → **Yes**

**Files Created/Modified**:
- `components.json` - ShadCN/UI configuration
- `lib/utils.ts` - Utility functions (cn function for classnames)
- `app/globals.css` - Updated with CSS variables

### Step 3: Install Required ShadCN/UI Components

Add all components needed for the application:

```bash
npx shadcn-ui@latest add button
npx shadcn-ui@latest add input
npx shadcn-ui@latest add card
npx shadcn-ui@latest add checkbox
npx shadcn-ui@latest add alert-dialog
npx shadcn-ui@latest add toast
npx shadcn-ui@latest add skeleton
```

**Components Installed** (in `components/ui/`):
- `button.tsx` - Form submit, edit, delete actions
- `input.tsx` - Todo description field
- `card.tsx` - Todo item container
- `checkbox.tsx` - Completion toggle
- `alert-dialog.tsx` - Delete confirmation modal
- `toast.tsx` + `toaster.tsx` + `use-toast.ts` - Notifications
- `skeleton.tsx` - Loading placeholders

### Step 4: Install Additional Dependencies

All required dependencies should now be installed. Verify `package.json`:

```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.0.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.0.0",
    "lucide-react": "^0.294.0",
    "@radix-ui/react-checkbox": "^1.0.4",
    "@radix-ui/react-alert-dialog": "^1.0.5",
    "@radix-ui/react-toast": "^1.1.5"
  }
}
```

Install dependencies (if not already done):

```bash
npm install
```

### Step 5: Configure Environment Variables

Create `.env.local` file in the `frontend/` directory:

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Note**: `.env.local` is gitignored by default (verified in `.gitignore`)

### Step 6: Create Folder Structure

Create the required directories:

```bash
mkdir -p app
mkdir -p components
mkdir -p lib
mkdir -p types
```

**Expected Structure**:
```
frontend/
├── app/
│   ├── layout.tsx   (already exists)
│   └── page.tsx     (will be replaced with todo UI)
├── components/
│   └── ui/          (ShadCN components - already exists)
├── lib/
│   ├── utils.ts     (already exists)
│   └── api.ts       (to be created during implementation)
├── types/
│   └── todo.ts      (to be created during implementation)
├── public/
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.js
├── components.json
└── .env.local
```

---

## Running the Application

### Step 1: Start Backend API

In a **separate terminal**, start the FastAPI backend:

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment (if using venv)
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Start backend server
uvicorn main:app --reload

# Expected output:
# INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
# INFO:     Started reloader process
```

**Verify Backend**:
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy"}
```

### Step 2: Start Frontend Development Server

In the **frontend directory**, start the Next.js dev server:

```bash
# From frontend/ directory
npm run dev

# Expected output:
#   ▲ Next.js 14.x.x
#   - Local:        http://localhost:3000
#   - Ready in 2.1s
```

### Step 3: Open Application in Browser

Navigate to:
```
http://localhost:3000
```

**Expected Initial State**:
- Empty state message: "No todos yet"
- Input form at top: "What needs to be done?"
- Add button enabled

---

## Development Workflow

### File Watching
Both servers support hot reload:
- **Backend**: `--reload` flag automatically restarts on Python file changes
- **Frontend**: Next.js Fast Refresh automatically updates browser on TypeScript/React changes

### Making Changes
1. Edit files in `frontend/app/`, `frontend/components/`, or `frontend/lib/`
2. Save file (Ctrl+S / Cmd+S)
3. Browser automatically refreshes with changes (~100-500ms)

### Stopping Servers
- **Backend**: Ctrl+C in backend terminal
- **Frontend**: Ctrl+C in frontend terminal

### Restarting
- **Backend**: `uvicorn main:app --reload`
- **Frontend**: `npm run dev`

---

## Manual Testing Guide

### Testing Checklist

Use this checklist to verify all features are working correctly. Test in browser at http://localhost:3000 with backend running.

---

#### 🎯 **User Story 1: View and Add Todos (P1)** - MVP Feature

**Scenario 1.1: Empty State Display**
- [ ] Open http://localhost:3000
- [ ] Verify empty state message appears: "No todos yet"
- [ ] Verify helpful subtext: "Add your first todo using the form above"
- [ ] Verify input form is visible at top of page

**Scenario 1.2: Add New Todo**
- [ ] Type "Buy groceries" in input field
- [ ] Click "Add Todo" button
- [ ] Verify todo appears in list below form
- [ ] Verify input field clears after submission
- [ ] Verify todo shows description "Buy groceries"
- [ ] Verify todo shows as incomplete (checkbox unchecked)

**Scenario 1.3: Fetch Existing Todos on Page Load**
- [ ] Create 3 todos: "Task 1", "Task 2", "Task 3"
- [ ] Refresh page (F5)
- [ ] Verify all 3 todos appear in list
- [ ] Verify todos maintain their order
- [ ] Verify completion status persists

**Scenario 1.4: Empty Description Validation**
- [ ] Leave input field empty
- [ ] Click "Add Todo" button
- [ ] Verify error message: "Description cannot be empty"
- [ ] Verify todo is NOT created
- [ ] Verify button is disabled when input is empty

**Scenario 1.5: Success Feedback**
- [ ] Type "Test todo" in input
- [ ] Click "Add Todo"
- [ ] Verify toast notification appears: "Todo created"
- [ ] Verify toast auto-dismisses after ~5 seconds
- [ ] Verify toast appears in bottom-right corner

**Scenario 1.6: Backend Offline Error**
- [ ] Stop backend server (Ctrl+C in backend terminal)
- [ ] Try to add a todo
- [ ] Verify error toast appears: "Connection error" / "Cannot reach the server"
- [ ] Verify todo is NOT added to list
- [ ] Restart backend and verify recovery

---

#### ✅ **User Story 2: Toggle Todo Completion (P2)**

**Scenario 2.1: Mark Todo as Complete**
- [ ] Create todo "Walk the dog"
- [ ] Click checkbox next to todo
- [ ] Verify immediate visual change (strikethrough or muted color)
- [ ] Verify checkbox shows checked state
- [ ] Verify change occurs within ~200ms (optimistic update)

**Scenario 2.2: Mark Todo as Incomplete**
- [ ] Click checkbox again on completed todo
- [ ] Verify visual indication removed (no strikethrough)
- [ ] Verify checkbox shows unchecked state
- [ ] Verify change occurs immediately

**Scenario 2.3: Completion Status Persists**
- [ ] Toggle todo completion to "complete"
- [ ] Refresh page (F5)
- [ ] Verify todo still shows as complete after reload
- [ ] Verify checkbox state persists

**Scenario 2.4: Optimistic Update with Success**
- [ ] Create todo and toggle completion
- [ ] Verify UI updates immediately (before server response)
- [ ] Verify success toast appears: "Todo updated"
- [ ] Verify final state matches server response

**Scenario 2.5: Optimistic Update with Rollback**
- [ ] Stop backend server
- [ ] Toggle todo completion
- [ ] Verify UI updates immediately (optimistic)
- [ ] Wait for error (~2-5 seconds)
- [ ] Verify UI reverts to previous state (rollback)
- [ ] Verify error toast appears: "Update failed"

**Scenario 2.6: Rapid Toggling (Race Condition Test)**
- [ ] Click checkbox rapidly 3-5 times
- [ ] Verify each click is processed
- [ ] Verify final state matches last click
- [ ] Verify no UI glitches or stuck states

---

#### ✏️ **User Story 3: Edit Todo Description (P3)**

**Scenario 3.1: Enter Edit Mode**
- [ ] Create todo "Buy milk"
- [ ] Click edit button (pencil icon)
- [ ] Verify description becomes editable input field
- [ ] Verify input is auto-focused (cursor in field)
- [ ] Verify save (check) and cancel (X) buttons appear

**Scenario 3.2: Save Edited Description**
- [ ] Enter edit mode
- [ ] Change description to "Buy milk and eggs"
- [ ] Click save button (check icon)
- [ ] Verify description updates in list
- [ ] Verify success toast appears: "Todo updated"
- [ ] Verify edit mode exits (back to view mode)

**Scenario 3.3: Empty Description Validation**
- [ ] Enter edit mode
- [ ] Clear description (empty input)
- [ ] Try to save
- [ ] Verify validation error appears
- [ ] Verify save button is disabled
- [ ] Verify edit is NOT saved

**Scenario 3.4: Cancel Edit**
- [ ] Enter edit mode
- [ ] Change description to "Something else"
- [ ] Click cancel button (X icon)
- [ ] Verify description reverts to original value
- [ ] Verify edit mode exits
- [ ] Verify no toast notification (no save occurred)

**Scenario 3.5: Edit with Backend Error**
- [ ] Stop backend server
- [ ] Enter edit mode and change description
- [ ] Click save
- [ ] Verify description reverts to original
- [ ] Verify error toast appears: "Update failed"
- [ ] Verify edit mode exits

**Scenario 3.6: Keyboard Shortcuts in Edit Mode**
- [ ] Enter edit mode
- [ ] Press Enter key
- [ ] Verify description saves (if valid)
- [ ] Enter edit mode again
- [ ] Press Escape key
- [ ] Verify edit cancels (reverts changes)

---

#### 🗑️ **User Story 4: Delete Todo (P3)**

**Scenario 4.1: Delete Confirmation Dialog**
- [ ] Create todo "Temporary task"
- [ ] Click delete button (trash icon)
- [ ] Verify confirmation dialog appears
- [ ] Verify dialog title: "Delete todo?"
- [ ] Verify dialog shows todo description
- [ ] Verify dialog has "Cancel" and "Delete" buttons

**Scenario 4.2: Cancel Deletion**
- [ ] Click delete button
- [ ] In confirmation dialog, click "Cancel"
- [ ] Verify dialog closes
- [ ] Verify todo remains in list
- [ ] Verify no toast notification

**Scenario 4.3: Confirm Deletion**
- [ ] Click delete button
- [ ] In confirmation dialog, click "Delete"
- [ ] Verify todo is removed from list
- [ ] Verify success toast appears: "Todo deleted"
- [ ] Verify dialog closes

**Scenario 4.4: Delete with Backend Error**
- [ ] Stop backend server
- [ ] Try to delete a todo
- [ ] Verify error toast appears: "Delete failed"
- [ ] Verify todo remains in list (not removed)
- [ ] Verify dialog closes

**Scenario 4.5: Delete Last Todo (Empty State)**
- [ ] Create single todo
- [ ] Delete the todo
- [ ] Verify empty state message appears: "No todos yet"
- [ ] Verify todo list is empty

---

#### ⏳ **User Story 5: Loading and Error States (P1)** - MVP Feature

**Scenario 5.1: Initial Loading Skeleton**
- [ ] Clear browser cache (Ctrl+Shift+Delete)
- [ ] Refresh page
- [ ] Verify skeleton loaders appear (3 placeholder items)
- [ ] Verify skeleton items match todo layout (checkbox + text)
- [ ] Verify skeletons have shimmer animation
- [ ] Verify skeletons disappear when data loads

**Scenario 5.2: Button Loading State During Create**
- [ ] Type todo description
- [ ] Click "Add Todo" button
- [ ] Verify button shows spinner icon
- [ ] Verify button text changes to "Adding..."
- [ ] Verify button is disabled during request
- [ ] Verify button returns to normal after response

**Scenario 5.3: Network Error Message**
- [ ] Stop backend server
- [ ] Try to load page (refresh)
- [ ] Verify error message appears: "Error loading todos"
- [ ] Verify error shows connection details
- [ ] Verify "Retry" button appears
- [ ] Click "Retry" (with backend running) and verify recovery

**Scenario 5.4: Server Error (500) Handling**
- [ ] (Requires backend modification to return 500)
- [ ] Trigger operation that returns 500
- [ ] Verify error toast appears: "Server error"
- [ ] Verify helpful message: "Please try again in a moment"

**Scenario 5.5: Loading Indicators for Mutations**
- [ ] Create a todo (verify button loading state)
- [ ] Toggle completion (verify optimistic update, no spinner)
- [ ] Delete a todo (verify "Deleting..." text in dialog button)
- [ ] Verify all loading states provide feedback within 500ms

---

#### 📱 **Responsive Design Testing**

**Mobile (320px - 639px)**
- [ ] Open Chrome DevTools (F12)
- [ ] Select "iPhone SE" or set width to 375px
- [ ] Verify all content fits without horizontal scroll
- [ ] Verify input and button are full-width stacked vertically
- [ ] Verify todo items display correctly
- [ ] Verify buttons have 44px minimum tap target (easy to tap)
- [ ] Verify text is readable without zoom (14px minimum)
- [ ] Verify spacing between interactive elements (no accidental taps)

**Tablet Portrait (640px - 767px)**
- [ ] Set viewport to 768px width
- [ ] Verify input and button switch to horizontal layout
- [ ] Verify todos display with adequate spacing
- [ ] Verify touch targets remain large (44px)

**Tablet Landscape / Desktop (768px+)**
- [ ] Set viewport to 1024px or larger
- [ ] Verify content centers with max-width (672px container)
- [ ] Verify padding increases for larger screens
- [ ] Verify hover states appear on buttons (desktop only)
- [ ] Verify text size increases slightly (16px)

**Large Desktop (1920px)**
- [ ] Set viewport to 1920px width
- [ ] Verify content remains centered (not stretched)
- [ ] Verify max-width container maintains readability
- [ ] Verify no layout issues at extreme width

---

### Testing Tools

**Browser DevTools**:
```
Chrome DevTools (F12)
├── Elements: Inspect HTML/CSS
├── Console: View errors and logs
├── Network: Monitor API requests/responses
├── Application: Check localStorage/sessionStorage
└── Device Toolbar (Ctrl+Shift+M): Test responsive design
```

**Manual API Testing**:
```bash
# Verify backend is responding
curl http://localhost:8000/health

# List all todos
curl http://localhost:8000/api/todos

# Create todo (manual)
curl -X POST http://localhost:8000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"description":"Test from curl"}'

# View in browser
open http://localhost:3000
```

**Network Throttling**:
1. Open DevTools → Network tab
2. Select throttling preset: "Slow 3G" or "Fast 3G"
3. Test loading states and optimistic updates
4. Verify skeleton loaders appear during slow loads
5. Reset to "No throttling" when done

---

## Troubleshooting

### Backend Connection Errors

**Problem**: Error toast "Cannot reach the server"

**Solutions**:
```bash
# 1. Verify backend is running
curl http://localhost:8000/health

# 2. Check backend logs for errors
# Look in terminal running uvicorn

# 3. Restart backend
cd backend
uvicorn main:app --reload

# 4. Check CORS configuration in backend/main.py
# Verify allow_origins includes "http://localhost:3000"
```

### ShadCN/UI Components Not Found

**Problem**: Import errors for ShadCN components

**Solutions**:
```bash
# 1. Verify components.json exists
cat components.json

# 2. Re-install missing component
npx shadcn-ui@latest add <component-name>

# 3. Check import paths
# Should be: import { Button } from "@/components/ui/button"
# NOT: import { Button } from "components/ui/button"

# 4. Verify tsconfig.json paths configuration
# Should include: "paths": { "@/*": ["./*"] }
```

### TypeScript Errors

**Problem**: Type errors in IDE or build

**Solutions**:
```bash
# 1. Restart TypeScript server in VS Code
# Cmd+Shift+P → "TypeScript: Restart TS Server"

# 2. Run type check
npm run build

# 3. Verify tsconfig.json has strict mode
# "strict": true should be present

# 4. Check for missing type definitions
npm install --save-dev @types/node @types/react @types/react-dom
```

### Port Already in Use

**Problem**: "Port 3000 is already in use"

**Solutions**:
```bash
# 1. Find process using port 3000
lsof -i :3000  # Mac/Linux
netstat -ano | findstr :3000  # Windows

# 2. Kill the process
kill -9 <PID>  # Mac/Linux
taskkill /PID <PID> /F  # Windows

# 3. Or use different port
npm run dev -- -p 3001
```

### Environment Variables Not Loading

**Problem**: API calls go to wrong URL

**Solutions**:
```bash
# 1. Verify .env.local exists and has correct content
cat .env.local
# Should contain: NEXT_PUBLIC_API_URL=http://localhost:8000

# 2. Restart Next.js dev server (env vars loaded at startup)
# Ctrl+C, then npm run dev

# 3. Check for typos
# Must be NEXT_PUBLIC_ prefix (not REACT_APP_)
```

### Styles Not Applying

**Problem**: Components render but have no styles

**Solutions**:
```bash
# 1. Verify Tailwind CSS is configured
cat tailwind.config.ts

# 2. Check globals.css is imported in layout.tsx
# Should have: import "./globals.css"

# 3. Restart dev server
npm run dev

# 4. Clear Next.js cache
rm -rf .next
npm run dev
```

---

## Build and Production

### Development Build (Type Check)

```bash
npm run build
```

**Expected Output**:
```
✓ Compiled successfully
✓ Linting and checking validity of types
✓ Collecting page data
✓ Generating static pages (3/3)
✓ Finalizing page optimization

Route (app)                              Size     First Load JS
┌ ○ /                                    5.2 kB         85.4 kB
└ ○ /_not-found                          871 B          81.1 kB
```

### Production Server

```bash
# Build for production
npm run build

# Start production server
npm start

# Expected: Server running on http://localhost:3000
```

### Environment Variables for Production

Create `.env.production.local`:
```bash
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

---

## Common Development Commands

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production (includes type check)
npm run build

# Start production server
npm start

# Run type check only
npm run type-check
# (Add to package.json: "type-check": "tsc --noEmit")

# Run linter
npm run lint

# Format code (if prettier configured)
npm run format
```

---

## Next Steps After Setup

1. **Implement Components** (see `tasks.md` for detailed breakdown)
   - Create TypeScript types in `types/todo.ts`
   - Implement API client in `lib/api.ts`
   - Build components in `components/` directory
   - Create main page in `app/page.tsx`

2. **Follow Task Sequence** (see `specs/002-frontend-todo-ui/tasks.md`)
   - Phase A: Project Setup (✅ COMPLETE with this guide)
   - Phase B: Foundational (Types + API Client)
   - Phase C-G: User Story Implementation (P1 → P2 → P3)
   - Phase H: Responsive Design & Polish
   - Phase I: Validation & Documentation

3. **Manual Testing** (Use checklist above after each phase)

4. **Commit and Push** (After each completed task or phase)
   ```bash
   git add .
   git commit -m "feat: implement user story X"
   git push origin 002-frontend-todo-ui
   ```

---

**Quickstart Guide Complete**: ✅
**Setup Status**: Ready for implementation
**Next Document**: tasks.md (generated by `/sp.tasks` command)
