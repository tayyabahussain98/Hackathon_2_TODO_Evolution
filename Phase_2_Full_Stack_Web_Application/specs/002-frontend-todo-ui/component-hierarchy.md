# Component Hierarchy: Frontend Todo UI

**Feature**: 002-frontend-todo-ui
**Date**: 2025-12-29
**Purpose**: Define component tree, responsibilities, props interfaces, and state management

---

## Architecture Overview

```
app/page.tsx (Root Page - State Container)
├── TodoForm (Create new todos)
├── LoadingSkeleton (Initial fetch loading)
├── EmptyState (No todos message)
└── TodoList (Display todos)
    └── TodoItem (Individual todo)
        ├── Checkbox (ShadCN/UI)
        ├── Input (ShadCN/UI - edit mode)
        ├── Button (ShadCN/UI - edit/delete actions)
        └── Dialog (ShadCN/UI - delete confirmation)

Toaster (ShadCN/UI - Toast notifications provider)
```

---

## Page Components

### app/page.tsx (Root Page)

**Purpose**: Main application container that manages global state and orchestrates all CRUD operations.

**State**:
```typescript
const [todos, setTodos] = useState<Todo[]>([]);
const [isLoading, setIsLoading] = useState(true);
const [error, setError] = useState<string | null>(null);
```

**Responsibilities**:
- Fetch todos on component mount (useEffect)
- Manage todos array state (create, update, delete operations)
- Coordinate mutations with API client
- Handle optimistic updates with rollback on error
- Display appropriate UI based on state (loading, error, empty, list)
- Provide toast notifications for user feedback

**Children**:
- `<TodoForm />` - Always rendered at top
- `<LoadingSkeleton />` - Rendered during initial fetch (isLoading === true)
- `<EmptyState />` - Rendered when todos.length === 0 && !isLoading
- `<TodoList />` - Rendered when todos.length > 0 && !isLoading

**Handlers**:
```typescript
// Create
async function handleCreateTodo(description: string): Promise<void> {
  const newTodo = await createTodo(description);
  setTodos((prev) => [newTodo, ...prev]); // Prepend new todo
  toast({ title: 'Todo created' });
}

// Toggle completion (optimistic)
async function handleToggleComplete(id: number, currentCompleted: boolean): Promise<void> {
  const previousTodos = [...todos];
  // Optimistic update
  setTodos((prev) => prev.map((todo) =>
    todo.id === id ? { ...todo, completed: !currentCompleted } : todo
  ));

  try {
    const updated = await updateTodo(id, { completed: !currentCompleted });
    setTodos((prev) => prev.map((todo) => todo.id === id ? updated : todo));
    toast({ title: 'Todo updated' });
  } catch (error) {
    setTodos(previousTodos); // Rollback
    toast({ title: 'Update failed', variant: 'destructive' });
  }
}

// Edit description
async function handleEditTodo(id: number, newDescription: string): Promise<void> {
  const updated = await updateTodo(id, { description: newDescription });
  setTodos((prev) => prev.map((todo) => todo.id === id ? updated : todo));
  toast({ title: 'Todo updated' });
}

// Delete
async function handleDeleteTodo(id: number): Promise<void> {
  await deleteTodo(id);
  setTodos((prev) => prev.filter((todo) => todo.id !== id));
  toast({ title: 'Todo deleted' });
}
```

**Layout**:
```tsx
<div className="container mx-auto px-4 py-8 max-w-2xl">
  <h1 className="text-3xl font-bold mb-8">My Todos</h1>

  <TodoForm onSubmit={handleCreateTodo} isSubmitting={isCreating} />

  {isLoading && <LoadingSkeleton count={3} />}

  {!isLoading && todos.length === 0 && <EmptyState />}

  {!isLoading && todos.length > 0 && (
    <TodoList
      todos={todos}
      onToggle={handleToggleComplete}
      onEdit={handleEditTodo}
      onDelete={handleDeleteTodo}
    />
  )}

  <Toaster />
</div>
```

---

## Feature Components

### TodoForm

**Purpose**: Input form for creating new todos with validation and loading state.

**Props**:
```typescript
interface TodoFormProps {
  onSubmit: (description: string) => Promise<void>;
  isSubmitting: boolean;
}
```

**State**:
```typescript
const [description, setDescription] = useState('');
const [error, setError] = useState<string | null>(null);
```

**Responsibilities**:
- Display Input field with placeholder "What needs to be done?"
- Validate description in real-time (onChange):
  - Not empty
  - Not exceeding 500 characters
- Show character counter when > 400 characters
- Display inline error messages
- Disable submit button when invalid or submitting
- Clear input after successful submission
- Handle form submission (preventDefault)

**Validation Rules**:
```typescript
const MIN_LENGTH = 1;
const MAX_LENGTH = 500;

function validate(value: string): string | null {
  if (value.trim().length === 0) {
    return 'Description cannot be empty';
  }
  if (value.length > MAX_LENGTH) {
    return `Description cannot exceed ${MAX_LENGTH} characters`;
  }
  return null;
}
```

**Layout**:
```tsx
<form onSubmit={handleSubmit} className="mb-6">
  <div className="flex flex-col sm:flex-row gap-3">
    <div className="flex-1">
      <Input
        value={description}
        onChange={handleChange}
        placeholder="What needs to be done?"
        disabled={isSubmitting}
        aria-invalid={!!error}
        aria-describedby={error ? 'input-error' : undefined}
        className="w-full"
      />
      {description.length > 400 && (
        <p className="text-xs text-muted-foreground mt-1">
          {description.length}/{MAX_LENGTH} characters
        </p>
      )}
      {error && (
        <p id="input-error" className="text-sm text-destructive mt-1">
          {error}
        </p>
      )}
    </div>
    <Button
      type="submit"
      disabled={isDisabled}
      className="w-full sm:w-auto"
    >
      {isSubmitting ? (
        <>
          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          Adding...
        </>
      ) : (
        'Add Todo'
      )}
    </Button>
  </div>
</form>
```

**Accessibility**:
- Input linked to error message via `aria-describedby`
- `aria-invalid` indicates validation state
- Button disabled state prevents invalid submissions
- Form semantic HTML for screen readers

---

### TodoList

**Purpose**: Container component that maps todos array to TodoItem components.

**Props**:
```typescript
interface TodoListProps {
  todos: Todo[];
  onToggle: (id: number, currentCompleted: boolean) => Promise<void>;
  onEdit: (id: number, newDescription: string) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
}
```

**State**: None (stateless presentation component)

**Responsibilities**:
- Map todos array to TodoItem components
- Pass down event handlers to children
- Maintain spacing between todo items
- Provide semantic list structure for accessibility

**Layout**:
```tsx
<div className="space-y-3" role="list">
  {todos.map((todo) => (
    <TodoItem
      key={todo.id}
      todo={todo}
      onToggle={onToggle}
      onEdit={onEdit}
      onDelete={onDelete}
    />
  ))}
</div>
```

**Notes**:
- Uses `space-y-3` for consistent 12px vertical spacing
- `role="list"` for screen reader semantics
- Each TodoItem receives unique key (todo.id)

---

### TodoItem

**Purpose**: Individual todo display with inline editing, completion toggle, and delete action.

**Props**:
```typescript
interface TodoItemProps {
  todo: Todo;
  onToggle: (id: number, currentCompleted: boolean) => Promise<void>;
  onEdit: (id: number, newDescription: string) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
}
```

**State**:
```typescript
const [isEditing, setIsEditing] = useState(false);
const [editedDescription, setEditedDescription] = useState(todo.description);
const [isDeleting, setIsDeleting] = useState(false);
const [showDeleteDialog, setShowDeleteDialog] = useState(false);
```

**Responsibilities**:
- Display todo description with completion status styling
- Toggle between view mode and edit mode
- Handle checkbox click for completion toggle (optimistic)
- Validate edited description before saving
- Show delete confirmation dialog before deletion
- Display loading states for edit/delete actions
- Handle edit cancel (revert to original description)

**View Mode Layout**:
```tsx
<Card className="p-3 md:p-4">
  <div className="flex items-center space-x-3 md:space-x-4">
    <Checkbox
      checked={todo.completed}
      onCheckedChange={() => onToggle(todo.id, todo.completed)}
      className="h-5 w-5 md:h-6 md:w-6"
      aria-label={`Mark "${todo.description}" as ${todo.completed ? 'incomplete' : 'complete'}`}
    />

    <span
      className={cn(
        'flex-1 text-sm md:text-base',
        todo.completed && 'line-through text-muted-foreground'
      )}
    >
      {todo.description}
    </span>

    <div className="flex space-x-2">
      <Button
        size="icon"
        variant="ghost"
        className="h-9 w-9 md:h-10 md:w-10"
        onClick={() => setIsEditing(true)}
        aria-label={`Edit "${todo.description}"`}
      >
        <Pencil className="h-4 w-4" />
      </Button>

      <Button
        size="icon"
        variant="ghost"
        className="h-9 w-9 md:h-10 md:w-10 text-destructive"
        onClick={() => setShowDeleteDialog(true)}
        aria-label={`Delete "${todo.description}"`}
      >
        <Trash2 className="h-4 w-4" />
      </Button>
    </div>
  </div>
</Card>
```

**Edit Mode Layout**:
```tsx
<Card className="p-3 md:p-4">
  <div className="flex items-center space-x-3 md:space-x-4">
    <Input
      value={editedDescription}
      onChange={(e) => setEditedDescription(e.target.value)}
      className="flex-1"
      autoFocus
      onKeyDown={(e) => {
        if (e.key === 'Enter') handleSave();
        if (e.key === 'Escape') handleCancel();
      }}
    />

    <div className="flex space-x-2">
      <Button
        size="icon"
        variant="ghost"
        className="h-9 w-9"
        onClick={handleSave}
        disabled={!isValidEdit}
      >
        <Check className="h-4 w-4 text-green-600" />
      </Button>

      <Button
        size="icon"
        variant="ghost"
        className="h-9 w-9"
        onClick={handleCancel}
      >
        <X className="h-4 w-4" />
      </Button>
    </div>
  </div>
</Card>
```

**Delete Confirmation Dialog**:
```tsx
<AlertDialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle>Delete todo?</AlertDialogTitle>
      <AlertDialogDescription>
        Are you sure you want to delete "{todo.description}"? This action cannot be undone.
      </AlertDialogDescription>
    </AlertDialogHeader>
    <AlertDialogFooter>
      <AlertDialogCancel>Cancel</AlertDialogCancel>
      <AlertDialogAction
        onClick={handleDelete}
        disabled={isDeleting}
        className="bg-destructive text-destructive-foreground"
      >
        {isDeleting ? 'Deleting...' : 'Delete'}
      </AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
```

**Handlers**:
```typescript
async function handleSave() {
  const trimmed = editedDescription.trim();
  if (trimmed.length === 0 || trimmed.length > 500) return;

  try {
    await onEdit(todo.id, trimmed);
    setIsEditing(false);
  } catch (error) {
    // Error handled by parent with toast
    setEditedDescription(todo.description); // Revert on error
  }
}

function handleCancel() {
  setEditedDescription(todo.description); // Revert changes
  setIsEditing(false);
}

async function handleDelete() {
  setIsDeleting(true);
  try {
    await onDelete(todo.id);
    setShowDeleteDialog(false);
  } catch (error) {
    // Error handled by parent with toast
  } finally {
    setIsDeleting(false);
  }
}
```

**Visual States**:
- **Completed**: Line-through text, muted color
- **Incomplete**: Normal text, full color
- **Editing**: Input replaces description, save/cancel buttons
- **Deleting**: Dialog open, delete button shows loading state

---

### EmptyState

**Purpose**: Display helpful message and call-to-action when no todos exist.

**Props**: None

**State**: None (static presentation component)

**Responsibilities**:
- Display friendly empty state message
- Show illustration or icon (optional)
- Provide guidance on how to add first todo

**Layout**:
```tsx
<Card className="p-8 md:p-12 text-center">
  <div className="flex flex-col items-center space-y-4">
    <div className="rounded-full bg-muted p-4">
      <CheckCircle2 className="h-12 w-12 text-muted-foreground" />
    </div>

    <div className="space-y-2">
      <h2 className="text-xl font-semibold">No todos yet</h2>
      <p className="text-muted-foreground">
        Add your first todo using the form above to get started!
      </p>
    </div>
  </div>
</Card>
```

**Notes**:
- Uses CheckCircle2 icon from lucide-react
- Muted colors to indicate empty state
- Centered layout with generous padding
- Responsive text sizing

---

### LoadingSkeleton

**Purpose**: Display skeleton placeholders during initial data fetch.

**Props**:
```typescript
interface LoadingSkeletonProps {
  count?: number; // Default: 3
}
```

**State**: None (static presentation component)

**Responsibilities**:
- Render skeleton placeholders matching TodoItem layout
- Show specified number of skeleton items
- Animate with shimmer effect (built into Skeleton component)

**Layout**:
```tsx
<div className="space-y-3" role="status" aria-label="Loading todos">
  {Array.from({ length: count }).map((_, index) => (
    <Card key={index} className="p-3 md:p-4">
      <div className="flex items-center space-x-3 md:space-x-4">
        <Skeleton className="h-5 w-5 md:h-6 md:w-6 rounded" /> {/* Checkbox */}
        <Skeleton className="h-4 flex-1 rounded" /> {/* Description */}
        <Skeleton className="h-9 w-9 md:h-10 md:w-10 rounded" /> {/* Edit button */}
        <Skeleton className="h-9 w-9 md:h-10 md:w-10 rounded" /> {/* Delete button */}
      </div>
    </Card>
  ))}
</div>
```

**Accessibility**:
- `role="status"` indicates loading region
- `aria-label` describes loading state
- Screen readers announce "Loading todos"

---

## ShadCN/UI Components Used

### Button
**Usage**: Form submit, edit, delete, save, cancel actions
**Variants**: `default`, `ghost`, `destructive`
**Sizes**: `default`, `icon`
**Props**: `disabled`, `onClick`, `type`, `aria-label`

### Input
**Usage**: Todo description field (create and edit)
**Props**: `value`, `onChange`, `placeholder`, `disabled`, `aria-invalid`, `aria-describedby`, `onKeyDown`, `autoFocus`

### Card
**Usage**: Todo item container, empty state container
**Props**: `className` (for padding and spacing)

### Checkbox
**Usage**: Toggle todo completion status
**Props**: `checked`, `onCheckedChange`, `aria-label`, `className`

### Dialog / AlertDialog
**Usage**: Delete confirmation modal
**Components**: `AlertDialog`, `AlertDialogContent`, `AlertDialogHeader`, `AlertDialogTitle`, `AlertDialogDescription`, `AlertDialogFooter`, `AlertDialogCancel`, `AlertDialogAction`
**Props**: `open`, `onOpenChange`, `disabled`

### Toast / Toaster
**Usage**: Success and error notifications
**Components**: `Toaster` (provider), `toast()` (function)
**Props**: `title`, `description`, `variant` (`default` | `destructive`)

### Skeleton
**Usage**: Loading placeholders during fetch
**Props**: `className` (for size and shape)

---

## State Management Summary

### Global State (app/page.tsx)
- `todos: Todo[]` - Array of all todos
- `isLoading: boolean` - Initial fetch loading state
- `error: string | null` - Global error state (unused if toast handles all errors)

### Component-Level State

**TodoForm**:
- `description: string` - Controlled input value
- `error: string | null` - Validation error message

**TodoItem**:
- `isEditing: boolean` - Edit mode toggle
- `editedDescription: string` - Temporary value during edit
- `isDeleting: boolean` - Delete loading state
- `showDeleteDialog: boolean` - Dialog open/close state

**No State** (Stateless Components):
- TodoList (pure presentation, maps props)
- EmptyState (static content)
- LoadingSkeleton (static placeholders)

---

## Data Flow Diagram

```
User Action → Component Handler → Parent Handler → API Client → Backend
                                      ↓
                                Update State
                                      ↓
                                Re-render UI
                                      ↓
                                Toast Feedback
```

**Example: Create Todo**
1. User types description in TodoForm Input
2. User clicks "Add Todo" Button
3. TodoForm calls `onSubmit(description)` prop
4. app/page.tsx `handleCreateTodo` calls `createTodo()` from api.ts
5. API client sends POST request to backend
6. Backend returns new Todo with ID
7. `handleCreateTodo` updates `todos` state with new todo
8. React re-renders TodoList with new todo
9. Toast notification shows "Todo created"
10. TodoForm clears input field

**Example: Toggle Completion (Optimistic)**
1. User clicks Checkbox in TodoItem
2. TodoItem calls `onToggle(id, currentCompleted)` prop
3. app/page.tsx `handleToggleComplete`:
   - Snapshots current todos array
   - Immediately updates todos state (optimistic)
   - Calls `updateTodo()` from api.ts
   - On success: Update state with server response, show toast
   - On error: Restore snapshot, show error toast

---

## Component File Structure

```
frontend/src/
├── app/
│   ├── layout.tsx          # Root layout with Toaster provider
│   └── page.tsx            # Main todo page (state container)
├── components/
│   ├── todo-form.tsx       # TodoForm component
│   ├── todo-list.tsx       # TodoList component
│   ├── todo-item.tsx       # TodoItem component
│   ├── empty-state.tsx     # EmptyState component
│   ├── loading-skeleton.tsx # LoadingSkeleton component
│   └── ui/                 # ShadCN/UI components (auto-generated)
│       ├── button.tsx
│       ├── input.tsx
│       ├── card.tsx
│       ├── checkbox.tsx
│       ├── dialog.tsx
│       ├── alert-dialog.tsx
│       ├── toast.tsx
│       ├── toaster.tsx
│       └── skeleton.tsx
├── lib/
│   ├── api.ts              # API client functions
│   └── utils.ts            # ShadCN utils (cn function)
└── types/
    └── todo.ts             # TypeScript interfaces
```

---

## Accessibility Features

1. **Semantic HTML**: `<form>`, `role="list"`, `role="status"`
2. **ARIA Labels**: All icon buttons have `aria-label` descriptions
3. **ARIA States**: `aria-invalid`, `aria-describedby` for form validation
4. **Keyboard Navigation**:
   - Enter key to save in edit mode
   - Escape key to cancel in edit mode
   - Tab navigation through all interactive elements
5. **Focus Management**: `autoFocus` on edit input when entering edit mode
6. **Loading Announcements**: `role="status"` for loading skeletons
7. **Error Announcements**: Toast notifications use ARIA live regions

---

## Performance Considerations

1. **Optimistic Updates**: <200ms feedback for toggle completion (no network wait)
2. **Component Memoization**: Not needed yet (small app, simple data flow)
3. **List Virtualization**: Not needed yet (no pagination, display all todos)
4. **Debouncing**: Not needed yet (no search/filter, single API calls)
5. **Bundle Size**: Native fetch reduces bundle vs axios (~13 KB savings)

---

**Component Hierarchy Complete**: ✅
**Next Artifact**: api-design.md (API client function signatures and types)
