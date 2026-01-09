# Quickstart Guide: Enhanced Todo Features

## Overview
This guide provides quick instructions for developers to understand and implement the enhanced todo features including priorities, tags, search, filter, sort, due dates, recurring tasks, and notifications.

## Database Setup

### Run Migrations
```bash
cd backend
alembic revision -m "add priority tags due_date recurrence to todos"
alembic upgrade head
```

### New Database Fields
The todos table will have these new columns:
- `priority`: ENUM('HIGH', 'MEDIUM', 'LOW') DEFAULT 'MEDIUM'
- `tags`: JSON field for storing array of tags
- `due_date`: TIMESTAMP NULL for due dates
- `recurrence_type`: ENUM('NONE', 'DAILY', 'WEEKLY', 'MONTHLY') DEFAULT 'NONE'
- `reminder_time`: INTEGER DEFAULT 10 for notification timing

## Backend Implementation

### 1. Update Todo Model
Update `models/todo.py` with new fields and validation.

### 2. Update Schemas
Update `schemas/todo.py` with new Pydantic models for request/response.

### 3. Update Service Layer
Enhance `services/todo_service.py` with:
- Search functionality (`search_todos`)
- Filter functionality (`filter_todos`)
- Sort functionality (`sort_todos`)
- Recurrence processing logic

### 4. Update API Routes
Enhance `routes/todos.py` with query parameters support and new functionality.

## Frontend Implementation

### 1. Update Todo Form
Enhance `components/todo-form.tsx` with:
- Priority selection dropdown
- Tags input component
- Due date picker
- Recurrence selection

### 2. Update Todo List
Enhance `components/todo-list.tsx` with:
- Search input field
- Filter controls (priority, status, tags)
- Sort controls dropdown

### 3. Update Todo Item
Enhance `components/todo-item.tsx` with:
- Priority visual indicators
- Due date display with overdue styling
- Tags display

### 4. Update API Client
Update `lib/api.ts` to support new fields and query parameters.

## Key Implementation Steps

### Phase 1: Intermediate Features
1. Add database schema changes
2. Implement backend search/filter/sort
3. Add frontend UI components
4. Test end-to-end functionality

### Phase 2: Advanced Features
1. Add due date functionality
2. Implement recurring tasks logic
3. Add browser notifications
4. Test advanced features

## API Query Examples

### Search and Filter
```javascript
// Search for todos containing "meeting"
fetch('/api/todos?search=meeting')

// Filter by priority and status
fetch('/api/todos?status=incomplete&priority=HIGH')

// Sort by due date
fetch('/api/todos?sort_by=due_date&order=asc')
```

### Create Todo with New Fields
```javascript
fetch('/api/todos', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token
  },
  body: JSON.stringify({
    description: 'New task',
    priority: 'HIGH',
    tags: ['work', 'urgent'],
    due_date: '2024-12-31T23:59:59Z',
    recurrence_type: 'NONE',
    reminder_time: 10
  })
})
```

## Testing Considerations

### Backend Tests
- Test new model validation
- Test search/filter/sort functionality
- Test recurrence logic
- Test API endpoint contracts

### Frontend Tests
- Test new form components
- Test search/filter UI
- Test due date validation
- Test notification handling

## Performance Notes

- Add proper database indexes for new fields
- Implement efficient search algorithms
- Consider pagination for large todo lists
- Optimize filtering and sorting operations