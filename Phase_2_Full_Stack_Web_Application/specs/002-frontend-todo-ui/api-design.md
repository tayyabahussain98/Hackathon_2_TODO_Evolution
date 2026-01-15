# API Client Design: Frontend Todo UI

**Feature**: 002-frontend-todo-ui
**Date**: 2025-12-29
**Purpose**: Define API client functions, TypeScript types, error handling, and backend integration patterns

---

## Configuration

**Base URL**:
```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
```

**Environment Variables** (`.env.local`):
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Request Headers**:
```typescript
{
  'Content-Type': 'application/json'
}
```

**Error Handling**: Parse `error.detail` from backend responses (FastAPI standard error format)

---

## TypeScript Type Definitions

### types/todo.ts

```typescript
/**
 * Todo entity matching backend response structure
 * Corresponds to TodoResponse in backend/models/todo.py
 */
export interface Todo {
  id: number;
  description: string;
  completed: boolean;
  created_at: string; // ISO 8601 format (UTC)
  updated_at: string; // ISO 8601 format (UTC)
}

/**
 * Request payload for creating a new todo
 * Corresponds to TodoCreate in backend/models/todo.py
 */
export interface CreateTodoRequest {
  description: string; // 1-500 characters
}

/**
 * Request payload for updating an existing todo
 * Corresponds to TodoUpdate in backend/models/todo.py
 * All fields optional - allows partial updates
 */
export interface UpdateTodoRequest {
  description?: string; // 1-500 characters if provided
  completed?: boolean;
}

/**
 * Backend error response structure
 * FastAPI returns { detail: string } for all errors
 */
export interface ApiError {
  detail: string;
}
```

---

## API Client Implementation

### lib/api.ts

```typescript
import {
  Todo,
  CreateTodoRequest,
  UpdateTodoRequest,
  ApiError,
} from '@/types/todo';

// Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Generic HTTP request wrapper with error handling and type safety
 *
 * @template T - Expected response type
 * @param endpoint - API endpoint path (e.g., '/api/todos')
 * @param options - Fetch API options (method, body, headers, etc.)
 * @returns Promise resolving to typed response data
 * @throws Error with backend error message or generic message
 */
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

    // Handle non-OK responses (4xx, 5xx)
    if (!response.ok) {
      // Try to parse error from backend
      const error: ApiError = await response.json().catch(() => ({
        detail: `HTTP ${response.status}: ${response.statusText}`,
      }));

      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    // Handle 204 No Content (DELETE responses)
    if (response.status === 204) {
      return undefined as T;
    }

    // Parse and return JSON response
    return await response.json();
  } catch (error) {
    // Re-throw Error instances (includes our custom errors above)
    if (error instanceof Error) {
      throw error;
    }

    // Handle unexpected errors (network failures, JSON parse errors)
    throw new Error('An unexpected error occurred. Please try again.');
  }
}

/**
 * Fetch all todos from the backend
 *
 * @returns Promise<Todo[]> - Array of all todos
 * @throws Error if request fails
 *
 * **Backend Endpoint**: GET /api/todos
 * **Success Response**: 200 OK with Todo[] body
 * **Error Responses**:
 *   - 500: Server error
 *   - Network error: Cannot reach server
 */
export async function fetchTodos(): Promise<Todo[]> {
  return apiRequest<Todo[]>('/api/todos', {
    method: 'GET',
  });
}

/**
 * Create a new todo
 *
 * @param description - Todo description (1-500 characters)
 * @returns Promise<Todo> - Created todo with generated ID and timestamps
 * @throws Error if validation fails or request fails
 *
 * **Backend Endpoint**: POST /api/todos
 * **Request Body**: { description: string }
 * **Success Response**: 201 Created with Todo body
 * **Error Responses**:
 *   - 400: Validation error (empty description or > 500 chars)
 *   - 500: Server error
 */
export async function createTodo(description: string): Promise<Todo> {
  const payload: CreateTodoRequest = { description };

  return apiRequest<Todo>('/api/todos', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

/**
 * Update an existing todo (partial update supported)
 *
 * @param id - Todo ID
 * @param updates - Fields to update (description and/or completed)
 * @returns Promise<Todo> - Updated todo with refreshed updated_at
 * @throws Error if todo not found or validation fails
 *
 * **Backend Endpoint**: PATCH /api/todos/{id}
 * **Request Body**: { description?: string, completed?: boolean }
 * **Success Response**: 200 OK with Todo body
 * **Error Responses**:
 *   - 400: Validation error (empty description if provided)
 *   - 404: Todo with given ID not found
 *   - 500: Server error
 */
export async function updateTodo(
  id: number,
  updates: UpdateTodoRequest
): Promise<Todo> {
  return apiRequest<Todo>(`/api/todos/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(updates),
  });
}

/**
 * Delete a todo
 *
 * @param id - Todo ID
 * @returns Promise<void> - Resolves with no data on success
 * @throws Error if todo not found or request fails
 *
 * **Backend Endpoint**: DELETE /api/todos/{id}
 * **Success Response**: 204 No Content (no body)
 * **Error Responses**:
 *   - 404: Todo with given ID not found
 *   - 500: Server error
 */
export async function deleteTodo(id: number): Promise<void> {
  return apiRequest<void>(`/api/todos/${id}`, {
    method: 'DELETE',
  });
}
```

---

## Error Handling Patterns

### Error Categorization

```typescript
/**
 * Enum for different error types to provide specific user feedback
 */
export enum ErrorType {
  NETWORK = 'network',      // Backend offline, CORS, DNS failures
  VALIDATION = 'validation', // 400 Bad Request (client-side validation)
  NOT_FOUND = 'not_found',   // 404 Not Found (resource doesn't exist)
  SERVER = 'server',         // 500 Internal Server Error
  UNKNOWN = 'unknown',       // Unexpected errors
}

/**
 * Categorize error based on message content
 *
 * @param error - Error object from API request
 * @returns ErrorType - Category of error for user feedback
 */
export function categorizeError(error: Error): ErrorType {
  const message = error.message.toLowerCase();

  // Network errors (fetch failures)
  if (
    message.includes('failed to fetch') ||
    message.includes('network') ||
    message.includes('cors')
  ) {
    return ErrorType.NETWORK;
  }

  // Validation errors (400 Bad Request)
  if (
    message.includes('400') ||
    message.includes('validation') ||
    message.includes('cannot be empty') ||
    message.includes('exceed')
  ) {
    return ErrorType.VALIDATION;
  }

  // Not found errors (404)
  if (message.includes('404') || message.includes('not found')) {
    return ErrorType.NOT_FOUND;
  }

  // Server errors (500)
  if (message.includes('500') || message.includes('server error')) {
    return ErrorType.SERVER;
  }

  return ErrorType.UNKNOWN;
}

/**
 * Get user-friendly error message based on error type
 *
 * @param error - Error object from API request
 * @returns Object with title and description for toast notification
 */
export function getErrorMessage(error: Error): {
  title: string;
  description: string;
} {
  const type = categorizeError(error);

  switch (type) {
    case ErrorType.NETWORK:
      return {
        title: 'Connection error',
        description:
          'Cannot reach the server. Please check your internet connection.',
      };

    case ErrorType.VALIDATION:
      return {
        title: 'Invalid input',
        description: error.message || 'Please check your input and try again.',
      };

    case ErrorType.NOT_FOUND:
      return {
        title: 'Not found',
        description: "The todo you're trying to modify no longer exists.",
      };

    case ErrorType.SERVER:
      return {
        title: 'Server error',
        description: 'Something went wrong. Please try again in a moment.',
      };

    case ErrorType.UNKNOWN:
    default:
      return {
        title: 'Error',
        description: error.message || 'An unexpected error occurred.',
      };
  }
}
```

### Usage in Components

```typescript
// Example: Using error handling in app/page.tsx
import { fetchTodos, createTodo, getErrorMessage } from '@/lib/api';
import { useToast } from '@/components/ui/use-toast';

function TodoPage() {
  const { toast } = useToast();

  async function handleCreateTodo(description: string) {
    try {
      const newTodo = await createTodo(description);
      setTodos((prev) => [newTodo, ...prev]);
      toast({ title: 'Success', description: 'Todo created' });
    } catch (error) {
      const { title, description } = getErrorMessage(error as Error);
      toast({ title, description, variant: 'destructive' });
    }
  }

  return (
    // Component JSX
  );
}
```

---

## API Contract Verification

### Backend Endpoint Mapping

| Frontend Function | Backend Endpoint | Method | Request Body | Success Response | Error Responses |
|-------------------|------------------|--------|--------------|------------------|-----------------|
| `fetchTodos()` | `/api/todos` | GET | None | 200 OK + Todo[] | 500 |
| `createTodo(description)` | `/api/todos` | POST | `{ description }` | 201 Created + Todo | 400, 500 |
| `updateTodo(id, updates)` | `/api/todos/{id}` | PATCH | `{ description?, completed? }` | 200 OK + Todo | 400, 404, 500 |
| `deleteTodo(id)` | `/api/todos/{id}` | DELETE | None | 204 No Content | 404, 500 |

### Type Alignment with Backend

| Frontend Type | Backend Model | Validation |
|---------------|---------------|------------|
| `Todo` | `TodoResponse` | ✅ Exact match (id, description, completed, created_at, updated_at) |
| `CreateTodoRequest` | `TodoCreate` | ✅ Exact match (description: string) |
| `UpdateTodoRequest` | `TodoUpdate` | ✅ Exact match (description?, completed?, both optional) |
| `ApiError` | FastAPI error format | ✅ Matches `{ detail: string }` structure |

**Validation Rules** (must match backend):
- Description: 1-500 characters (validated client-side before request)
- Description: Cannot be empty string (validated client-side before request)
- Completed: Boolean only (true/false)
- Timestamps: ISO 8601 format (backend generates, frontend displays as-is)

---

## Request/Response Examples

### Create Todo

**Request**:
```http
POST http://localhost:8000/api/todos
Content-Type: application/json

{
  "description": "Buy groceries"
}
```

**Success Response (201 Created)**:
```json
{
  "id": 1,
  "description": "Buy groceries",
  "completed": false,
  "created_at": "2025-12-29T10:30:00Z",
  "updated_at": "2025-12-29T10:30:00Z"
}
```

**Error Response (400 Bad Request)**:
```json
{
  "detail": "Description cannot be empty"
}
```

### Fetch All Todos

**Request**:
```http
GET http://localhost:8000/api/todos
```

**Success Response (200 OK)**:
```json
[
  {
    "id": 1,
    "description": "Buy groceries",
    "completed": false,
    "created_at": "2025-12-29T10:30:00Z",
    "updated_at": "2025-12-29T10:30:00Z"
  },
  {
    "id": 2,
    "description": "Walk the dog",
    "completed": true,
    "created_at": "2025-12-29T09:15:00Z",
    "updated_at": "2025-12-29T11:00:00Z"
  }
]
```

**Empty Response (200 OK)**:
```json
[]
```

### Update Todo

**Request (Toggle Completion)**:
```http
PATCH http://localhost:8000/api/todos/1
Content-Type: application/json

{
  "completed": true
}
```

**Success Response (200 OK)**:
```json
{
  "id": 1,
  "description": "Buy groceries",
  "completed": true,
  "created_at": "2025-12-29T10:30:00Z",
  "updated_at": "2025-12-29T11:15:00Z"
}
```

**Request (Edit Description)**:
```http
PATCH http://localhost:8000/api/todos/1
Content-Type: application/json

{
  "description": "Buy groceries and milk"
}
```

**Error Response (404 Not Found)**:
```json
{
  "detail": "Todo with id 999 not found"
}
```

### Delete Todo

**Request**:
```http
DELETE http://localhost:8000/api/todos/1
```

**Success Response (204 No Content)**:
```
(No body)
```

**Error Response (404 Not Found)**:
```json
{
  "detail": "Todo with id 999 not found"
}
```

---

## CORS Configuration (Backend)

**Note**: Backend must allow CORS for frontend origin.

**Required Backend Configuration** (backend/main.py):
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
```

**Production Configuration**:
```python
# Update allow_origins with production frontend URL
allow_origins=[
    "http://localhost:3000",  # Development
    "https://yourdomain.com"   # Production
]
```

---

## Testing the API Client

### Manual Testing Checklist

**Prerequisites**: Backend running at http://localhost:8000

```bash
# Test backend health
curl http://localhost:8000/health
# Expected: { "status": "healthy" }

# Test fetch todos (empty)
curl http://localhost:8000/api/todos
# Expected: []

# Test create todo
curl -X POST http://localhost:8000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"description":"Test todo"}'
# Expected: 201 with todo object

# Test fetch todos (with data)
curl http://localhost:8000/api/todos
# Expected: [{ "id": 1, ... }]

# Test update todo
curl -X PATCH http://localhost:8000/api/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'
# Expected: 200 with updated todo

# Test delete todo
curl -X DELETE http://localhost:8000/api/todos/1
# Expected: 204 No Content

# Test 404 error
curl http://localhost:8000/api/todos/999
# Expected: 404 with error message
```

### Integration Testing in Frontend

```typescript
// Test in browser console or Next.js page
import { fetchTodos, createTodo, updateTodo, deleteTodo } from '@/lib/api';

// Test sequence
async function testApi() {
  try {
    console.log('1. Fetch todos (empty)');
    const empty = await fetchTodos();
    console.log('Result:', empty); // []

    console.log('2. Create todo');
    const newTodo = await createTodo('Test from frontend');
    console.log('Created:', newTodo); // { id: 1, description: '...', ... }

    console.log('3. Fetch todos (with data)');
    const todos = await fetchTodos();
    console.log('Todos:', todos); // [{ id: 1, ... }]

    console.log('4. Update todo');
    const updated = await updateTodo(newTodo.id, { completed: true });
    console.log('Updated:', updated); // { id: 1, completed: true, ... }

    console.log('5. Delete todo');
    await deleteTodo(newTodo.id);
    console.log('Deleted successfully'); // undefined (no return value)

    console.log('6. Verify deletion');
    const afterDelete = await fetchTodos();
    console.log('After delete:', afterDelete); // []

    console.log('✅ All tests passed!');
  } catch (error) {
    console.error('❌ Test failed:', error);
  }
}
```

---

## Performance Considerations

### Bundle Size
- **Native fetch**: 0 KB (built into browser)
- **Alternative (axios)**: ~13 KB gzipped
- **Savings**: ~13 KB by using native fetch

### Request Optimization
- No automatic retries (user must manually retry on error)
- No request caching (fetch fresh data on every call)
- No request deduplication (multiple simultaneous requests allowed)

**Rationale**: Simple CRUD app doesn't require advanced features. Can add libraries later if needed.

### Type Safety
- All API functions return typed Promises
- TypeScript compiler catches type mismatches at build time
- Generic `apiRequest<T>` ensures response types match expectations

---

## Future Enhancements (Out of Scope for This Phase)

1. **Request Caching**: Use SWR or React Query for automatic caching
2. **Request Retries**: Exponential backoff for transient failures
3. **Request Cancellation**: AbortController for cancelled navigations
4. **Optimistic Updates**: Move pattern into API client for reusability
5. **Request Deduplication**: Prevent duplicate simultaneous requests
6. **Offline Support**: Queue mutations when offline, sync when online
7. **Authentication**: Add JWT token to request headers
8. **Rate Limiting**: Client-side rate limiting to prevent abuse

---

**API Design Complete**: ✅
**Next Artifact**: quickstart.md (Setup and running instructions)
