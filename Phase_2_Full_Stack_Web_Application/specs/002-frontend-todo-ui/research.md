# Research & Technical Decisions: Frontend Todo UI

**Feature**: 002-frontend-todo-ui
**Date**: 2025-12-29
**Purpose**: Document technical decisions and implementation patterns before design phase

---

## R1: Next.js 14 App Router Setup

**Decision**: Use `create-next-app@latest` with TypeScript, Tailwind CSS, and App Router enabled.

**Rationale**:
- `create-next-app` provides officially supported, battle-tested setup
- App Router is the recommended approach for Next.js 14+ (Pages Router is legacy)
- TypeScript strict mode catches errors early and provides better IDE support
- Tailwind CSS integration is seamless with Next.js and matches ShadCN/UI requirements

**Alternatives Considered**:
1. **Manual setup** - Rejected: Error-prone, requires deep knowledge of Next.js configuration files
2. **Pages Router** - Rejected: Legacy approach, doesn't leverage latest Next.js features (Server Components, streaming)
3. **Vite + React** - Rejected: Doesn't provide SSR/SSG capabilities, more configuration overhead

**Implementation Notes**:
```bash
# Initialization command
npx create-next-app@latest frontend --typescript --tailwind --app --no-src-dir --import-alias "@/*"

# Key configuration files created:
# - next.config.js: Next.js configuration
# - tsconfig.json: TypeScript strict mode enabled
# - tailwind.config.ts: Tailwind CSS configuration
# - app/layout.tsx: Root layout with metadata
# - app/page.tsx: Home page component
```

**TypeScript Configuration (tsconfig.json)**:
```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "jsx": "preserve",
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "paths": { "@/*": ["./*"] }
  }
}
```

---

## R2: ShadCN/UI Integration

**Decision**: Use ShadCN/UI CLI to install individual components with "New York" style and "Neutral" color theme.

**Rationale**:
- ShadCN/UI provides copy-paste components (not npm package), giving full control over code
- Built on Radix UI primitives, ensuring accessibility (WCAG 2.1 AA baseline)
- Tailwind CSS based, matches our styling approach
- Components are customizable and can be modified directly in codebase
- Active community and excellent documentation

**Alternatives Considered**:
1. **Material UI (MUI)** - Rejected: Heavy bundle size, opinionated design, harder to customize
2. **Chakra UI** - Rejected: CSS-in-JS approach conflicts with Tailwind, larger bundle
3. **Raw Radix UI** - Rejected: Requires extensive styling work, no pre-built patterns
4. **Ant Design** - Rejected: Not Tailwind-based, complex theming system

**Implementation Notes**:
```bash
# Initialize ShadCN/UI
npx shadcn-ui@latest init

# Configuration choices:
# - Style: New York (clean, minimal aesthetic)
# - Color: Neutral (professional gray palette)
# - CSS variables: Yes (enables theme customization)
# - Tailwind config: Yes (auto-configures paths)

# Install required components individually
npx shadcn-ui@latest add button
npx shadcn-ui@latest add input
npx shadcn-ui@latest add card
npx shadcn-ui@latest add checkbox
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add toast
npx shadcn-ui@latest add skeleton

# Components installed to: components/ui/
# Each component is a .tsx file with full source code
```

**Components Needed and Their Usage**:
- **Button**: Form submit, edit, delete actions
- **Input**: Todo description text field
- **Card**: Todo item container for visual separation
- **Checkbox**: Toggle todo completion status
- **Dialog**: Delete confirmation modal (AlertDialog variant)
- **Toast**: Success and error notifications (with Toaster provider)
- **Skeleton**: Loading placeholders during data fetch

---

## R3: API Client Architecture

**Decision**: Use native `fetch()` API with TypeScript generics for type-safe requests.

**Rationale**:
- Native fetch is built into modern browsers (Chrome 42+, Firefox 39+)
- Zero dependencies = smaller bundle size (~0 KB vs axios ~13 KB)
- Sufficient for simple CRUD operations (no need for advanced features)
- TypeScript generics provide type safety for request/response
- Async/await syntax is clean and readable

**Alternatives Considered**:
1. **axios** - Rejected: Adds 13 KB gzipped, overkill for simple REST API, brings interceptors we don't need yet
2. **ky** - Rejected: Smaller than axios (5 KB) but still adds dependency when fetch suffices
3. **react-query** - Rejected: Powerful caching/state management but violates "no state library" constraint
4. **SWR** - Rejected: Same reason as react-query, adds complexity we don't need

**Implementation Notes**:

```typescript
// lib/api.ts structure

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface ApiError {
  detail: string;
}

// Generic request wrapper with error handling
async function apiRequest<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    // Handle non-OK responses
    if (!response.ok) {
      const error: ApiError = await response.json().catch(() => ({
        detail: `HTTP ${response.status}: ${response.statusText}`,
      }));
      throw new Error(error.detail);
    }

    // Handle 204 No Content (delete responses)
    if (response.status === 204) {
      return undefined as T;
    }

    return await response.json();
  } catch (error) {
    // Network errors or JSON parsing failures
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('An unexpected error occurred');
  }
}

// Type-safe API functions
export async function fetchTodos(): Promise<Todo[]> {
  return apiRequest<Todo[]>('/api/todos');
}

export async function createTodo(description: string): Promise<Todo> {
  return apiRequest<Todo>('/api/todos', {
    method: 'POST',
    body: JSON.stringify({ description }),
  });
}

export async function updateTodo(
  id: number,
  updates: { description?: string; completed?: boolean }
): Promise<Todo> {
  return apiRequest<Todo>(`/api/todos/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(updates),
  });
}

export async function deleteTodo(id: number): Promise<void> {
  return apiRequest<void>(`/api/todos/${id}`, {
    method: 'DELETE',
  });
}
```

**Environment Variable**:
- Create `.env.local`: `NEXT_PUBLIC_API_URL=http://localhost:8000`
- Fallback to localhost:8000 for development
- Production deployment will override with actual backend URL

---

## R4: Optimistic Update Pattern

**Decision**: Snapshot state before mutation, apply optimistic update immediately, rollback on error with toast notification.

**Rationale**:
- Optimistic updates provide instant feedback (<200ms requirement)
- Users perceive faster response time even when network is slow
- Rollback mechanism maintains data consistency on errors
- Try/catch pattern is straightforward and maintainable
- Matches common React patterns (no custom hooks needed)

**Alternatives Considered**:
1. **Wait for server response** - Rejected: Slow UX, violates SC-003 (200ms requirement)
2. **Custom useOptimistic hook** - Rejected: Over-engineering for simple CRUD operations
3. **Optimistic without rollback** - Rejected: Leaves UI in inconsistent state on errors
4. **Queue mutations** - Rejected: Too complex for single-user app without offline support

**Implementation Notes**:

```typescript
// Pattern for toggle completion (optimistic update)
async function handleToggleComplete(id: number, currentCompleted: boolean) {
  // 1. Snapshot current state for rollback
  const previousTodos = [...todos];

  // 2. Apply optimistic update immediately
  const optimisticTodos = todos.map((todo) =>
    todo.id === id
      ? { ...todo, completed: !currentCompleted, updated_at: new Date().toISOString() }
      : todo
  );
  setTodos(optimisticTodos);

  try {
    // 3. Send mutation to backend
    const updatedTodo = await updateTodo(id, { completed: !currentCompleted });

    // 4. Replace optimistic update with server response
    setTodos((current) =>
      current.map((todo) => (todo.id === id ? updatedTodo : todo))
    );

    // 5. Success feedback
    toast({
      title: 'Todo updated',
      description: `Marked as ${updatedTodo.completed ? 'complete' : 'incomplete'}`,
    });
  } catch (error) {
    // 6. Rollback on error
    setTodos(previousTodos);

    // 7. Error feedback
    toast({
      title: 'Update failed',
      description: error instanceof Error ? error.message : 'Please try again',
      variant: 'destructive',
    });
  }
}
```

**Key Points**:
- State snapshot must be shallow copy (`[...todos]`) to preserve original
- Optimistic update uses temporary timestamp for UI purposes
- Server response overwrites optimistic data with authoritative values
- Rollback restores exact previous state (no partial updates)
- Toast provides feedback for both success and error cases

---

## R5: Error Handling Strategy

**Decision**: Use ShadCN Toast component for all user-facing error messages, differentiate network errors from validation errors.

**Rationale**:
- ShadCN Toast is already part of component library (no extra dependency)
- Non-blocking notification system (doesn't interrupt workflow)
- Supports variants (default, destructive) for success vs error
- Auto-dismisses after 5 seconds (configurable)
- Accessible (ARIA live regions, keyboard navigation)

**Alternatives Considered**:
1. **react-hot-toast** - Rejected: Additional dependency (4 KB), similar features to ShadCN Toast
2. **Alert components inline** - Rejected: Blocks UI flow, requires manual dismissal
3. **Console.error only** - Rejected: Not user-facing, poor UX
4. **Modal dialogs** - Rejected: Too disruptive for transient errors

**Implementation Notes**:

```typescript
// Error categorization
enum ErrorType {
  NETWORK = 'network',      // Backend offline, CORS, DNS
  VALIDATION = 'validation', // 400 Bad Request
  NOT_FOUND = 'not_found',   // 404 Not Found
  SERVER = 'server',         // 500 Internal Server Error
}

function categorizeError(error: Error): ErrorType {
  const message = error.message.toLowerCase();

  if (message.includes('failed to fetch') || message.includes('network')) {
    return ErrorType.NETWORK;
  }
  if (message.includes('400') || message.includes('validation')) {
    return ErrorType.VALIDATION;
  }
  if (message.includes('404') || message.includes('not found')) {
    return ErrorType.NOT_FOUND;
  }
  return ErrorType.SERVER;
}

// User-friendly error messages
function getErrorMessage(error: Error): { title: string; description: string } {
  const type = categorizeError(error);

  switch (type) {
    case ErrorType.NETWORK:
      return {
        title: 'Connection error',
        description: 'Cannot reach the server. Please check your internet connection.',
      };
    case ErrorType.VALIDATION:
      return {
        title: 'Invalid input',
        description: error.message || 'Please check your input and try again.',
      };
    case ErrorType.NOT_FOUND:
      return {
        title: 'Not found',
        description: 'The todo you\'re trying to modify no longer exists.',
      };
    case ErrorType.SERVER:
      return {
        title: 'Server error',
        description: 'Something went wrong. Please try again in a moment.',
      };
  }
}

// Usage in components
try {
  await createTodo(description);
  toast({ title: 'Success', description: 'Todo created' });
} catch (error) {
  const { title, description } = getErrorMessage(error as Error);
  toast({ title, description, variant: 'destructive' });
}
```

**Toast Configuration**:
- Position: Bottom-right corner (non-intrusive)
- Duration: 5000ms for success, 7000ms for errors (more time to read)
- Dismissible: Yes (close button + auto-dismiss)
- Multiple toasts: Stack vertically

---

## R6: Form Validation

**Decision**: Use controlled inputs with `onChange` validation for real-time feedback, prevent submission with disabled button state.

**Rationale**:
- Real-time validation provides immediate feedback (better UX)
- Controlled inputs give React full control over input state
- Disabled button prevents invalid submissions (no need for form libraries)
- Client-side validation reduces unnecessary backend requests
- Simple enough that validation libraries (zod, yup) are overkill

**Alternatives Considered**:
1. **react-hook-form** - Rejected: 24 KB dependency for simple validation, over-engineered
2. **Formik** - Rejected: Heavy (40 KB), complex API for our use case
3. **onSubmit validation only** - Rejected: Poor UX, user doesn't know about errors until submit
4. **Server-side validation only** - Rejected: Slow feedback, wastes backend resources

**Implementation Notes**:

```typescript
// TodoForm component validation pattern
function TodoForm({ onSubmit, isSubmitting }: TodoFormProps) {
  const [description, setDescription] = useState('');
  const [error, setError] = useState<string | null>(null);

  // Validation rules
  const MIN_LENGTH = 1;
  const MAX_LENGTH = 500;

  // Real-time validation on change
  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const value = e.target.value;
    setDescription(value);

    // Validate and set error message
    if (value.length === 0) {
      setError('Description cannot be empty');
    } else if (value.length > MAX_LENGTH) {
      setError(`Description cannot exceed ${MAX_LENGTH} characters`);
    } else {
      setError(null);
    }
  }

  // Submit handler
  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    // Final validation check
    if (error || description.trim().length === 0) {
      return;
    }

    try {
      await onSubmit(description.trim());
      setDescription(''); // Clear input on success
      setError(null);
    } catch (err) {
      // Error handled by parent component with toast
    }
  }

  // Determine if submit should be disabled
  const isDisabled = isSubmitting || !!error || description.trim().length === 0;

  return (
    <form onSubmit={handleSubmit}>
      <Input
        value={description}
        onChange={handleChange}
        placeholder="What needs to be done?"
        disabled={isSubmitting}
        aria-invalid={!!error}
        aria-describedby={error ? 'input-error' : undefined}
      />
      {error && (
        <p id="input-error" className="text-sm text-destructive mt-1">
          {error}
        </p>
      )}
      <Button type="submit" disabled={isDisabled}>
        {isSubmitting ? 'Adding...' : 'Add Todo'}
      </Button>
    </form>
  );
}
```

**Validation Rules**:
1. **Empty check**: `description.trim().length > 0`
2. **Max length**: `description.length <= 500`
3. **Character counter**: Display `{description.length}/500` when > 400 characters

**Accessibility**:
- `aria-invalid` on Input when error exists
- `aria-describedby` links input to error message
- Error message has unique ID for screen readers
- Disabled button prevents invalid submissions (visual + functional)

---

## R7: Loading State Management

**Decision**: Use component-level loading states with ShadCN Skeleton for initial fetch, button loading states for mutations.

**Rationale**:
- Component-level state is simpler than global loading management
- Skeleton loaders match content layout (better UX than spinners)
- Button loading states provide context-specific feedback
- No need for global loading library (reduces complexity)
- Each component controls its own loading UX

**Alternatives Considered**:
1. **Global loading context** - Rejected: Overkill for single-page app, adds complexity
2. **Loading spinner overlay** - Rejected: Blocks entire UI, poor UX for partial loading
3. **No loading states** - Rejected: Violates requirements, confusing for users
4. **react-loading-skeleton** - Rejected: Redundant when ShadCN provides Skeleton component

**Implementation Notes**:

```typescript
// Initial fetch loading pattern (page.tsx)
function TodoPage() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadTodos() {
      try {
        setIsLoading(true);
        const data = await fetchTodos();
        setTodos(data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load todos');
      } finally {
        setIsLoading(false);
      }
    }
    loadTodos();
  }, []);

  // Render loading skeleton
  if (isLoading) {
    return <LoadingSkeleton count={3} />;
  }

  // Render error state
  if (error) {
    return (
      <div className="text-destructive">
        <p>Error loading todos: {error}</p>
        <Button onClick={() => window.location.reload()}>Retry</Button>
      </div>
    );
  }

  return <TodoList todos={todos} />;
}

// LoadingSkeleton component
function LoadingSkeleton({ count = 3 }: { count?: number }) {
  return (
    <div className="space-y-3">
      {Array.from({ length: count }).map((_, i) => (
        <Card key={i} className="p-4">
          <div className="flex items-center space-x-4">
            <Skeleton className="h-5 w-5" /> {/* Checkbox placeholder */}
            <Skeleton className="h-4 w-3/4" /> {/* Description placeholder */}
          </div>
        </Card>
      ))}
    </div>
  );
}

// Button loading pattern (mutation)
function TodoForm({ onSubmit }: TodoFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(description: string) {
    setIsSubmitting(true);
    try {
      await onSubmit(description);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <Button type="submit" disabled={isSubmitting}>
      {isSubmitting ? (
        <>
          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          Adding...
        </>
      ) : (
        'Add Todo'
      )}
    </Button>
  );
}
```

**Loading Patterns**:
1. **Initial fetch**: Skeleton loaders (3 placeholder items)
2. **Create todo**: Button shows spinner + "Adding..." text
3. **Update todo**: Button shows spinner + "Updating..." text (if separate button)
4. **Delete todo**: Dialog button shows spinner + "Deleting..." text
5. **Optimistic updates**: No loading state (instant feedback)

**Skeleton Design**:
- Match actual content layout (checkbox + text)
- Animate with shimmer effect (Skeleton component default)
- Use same Card container as real todos
- Show 3 items by default (reasonable placeholder count)

---

## R8: Responsive Design Approach

**Decision**: Use Tailwind CSS mobile-first approach with default breakpoints, 44px minimum touch targets for mobile interactions.

**Rationale**:
- Mobile-first ensures base styles work on smallest screens
- Tailwind breakpoints are industry-standard (sm: 640px, md: 768px, lg: 1024px)
- 44px touch targets meet Apple Human Interface Guidelines and Material Design specs
- Flexbox and Grid utilities handle responsive layouts without media queries
- Container queries not needed for single-page app

**Alternatives Considered**:
1. **Desktop-first** - Rejected: Harder to scale down, mobile is majority traffic
2. **Custom breakpoints** - Rejected: Tailwind defaults cover 320px-1920px requirement
3. **CSS Grid only** - Rejected: Flexbox is simpler for single-column mobile layouts
4. **Responsive libraries (react-responsive)** - Rejected: Tailwind utilities are sufficient

**Implementation Notes**:

**Tailwind Breakpoints** (used with mobile-first approach):
```typescript
// Default Tailwind breakpoints (no customization needed)
{
  'sm': '640px',  // Tablet portrait
  'md': '768px',  // Tablet landscape
  'lg': '1024px', // Desktop
  'xl': '1280px', // Large desktop
  '2xl': '1536px' // Extra large desktop
}
```

**Responsive Layout Patterns**:

```tsx
// Page layout (app/page.tsx)
<div className="container mx-auto px-4 py-8 max-w-2xl">
  {/* Mobile: full width with padding */}
  {/* Desktop: centered with max-width */}
  <TodoForm />
  <TodoList />
</div>

// TodoItem component (responsive)
<Card className="p-3 md:p-4">
  {/* Mobile: 12px padding, Desktop: 16px padding */}
  <div className="flex items-center space-x-3 md:space-x-4">
    {/* Mobile: 12px gap, Desktop: 16px gap */}
    <Checkbox className="h-5 w-5 md:h-6 md:w-6" />
    {/* Mobile: 20px touch target, Desktop: 24px */}
    <span className="flex-1 text-sm md:text-base">{description}</span>
    {/* Mobile: 14px text, Desktop: 16px text */}
    <div className="flex space-x-2">
      <Button size="icon" className="h-9 w-9 md:h-10 md:w-10">
        {/* 44px minimum touch target on mobile */}
        <Pencil className="h-4 w-4" />
      </Button>
      <Button size="icon" variant="destructive" className="h-9 w-9 md:h-10 md:w-10">
        <Trash2 className="h-4 w-4" />
      </Button>
    </div>
  </div>
</Card>

// TodoForm (responsive)
<form className="flex flex-col sm:flex-row gap-3 mb-6">
  {/* Mobile: vertical stack, Tablet+: horizontal row */}
  <Input
    className="flex-1"
    placeholder="What needs to be done?"
  />
  <Button type="submit" className="w-full sm:w-auto">
    {/* Mobile: full width, Tablet+: auto width */}
    Add Todo
  </Button>
</form>
```

**Touch Target Guidelines**:
- **Buttons**: Minimum 44x44px (`h-11 w-11` = 44px in Tailwind)
- **Checkboxes**: Minimum 44x44px total tap area (use padding/margin)
- **Links/Actions**: Minimum 44x44px tap area
- **Spacing**: 8px minimum between touch targets

**Responsive Breakpoint Strategy**:
- **320px-639px (Mobile)**: Single column, full-width buttons, 44px touch targets, 12px spacing
- **640px-767px (Tablet Portrait)**: Horizontal form layout, slightly larger text
- **768px+ (Tablet Landscape/Desktop)**: Max-width container (672px), 16px spacing, hover states

**Testing Strategy**:
```bash
# Browser DevTools responsive mode
- iPhone SE (375x667) - Smallest common mobile
- iPad (768x1024) - Tablet
- Desktop (1920x1080) - Large desktop

# Manual test checklist:
- [ ] All buttons tappable without zoom
- [ ] Text readable without zoom (min 14px)
- [ ] No horizontal scroll
- [ ] Forms usable with on-screen keyboard
- [ ] Spacing between interactive elements adequate
```

---

## Summary of Decisions

| Decision | Technology/Pattern | Rationale |
|----------|-------------------|-----------|
| R1 | Next.js 14 App Router (create-next-app) | Official setup, TypeScript + Tailwind integration |
| R2 | ShadCN/UI (New York style, Neutral) | Accessible, customizable, Tailwind-based |
| R3 | Native fetch() with TypeScript generics | Zero dependencies, sufficient for CRUD |
| R4 | Optimistic updates with rollback | <200ms feedback, maintains consistency |
| R5 | ShadCN Toast for all errors | Non-blocking, accessible, categorized messages |
| R6 | Controlled inputs with onChange validation | Real-time feedback, disabled button prevents invalid submit |
| R7 | Component-level loading (Skeleton + Button states) | Contextual feedback, no global complexity |
| R8 | Mobile-first Tailwind (44px touch targets) | Industry standards, covers 320px-1920px |

**All Research Complete**: ✅
**Next Phase**: Phase 1 (Design & Contracts) - Generate component-hierarchy.md, api-design.md, quickstart.md
