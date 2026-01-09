# Data Model: Enhanced Todo Features

## Entity: Todo

### Fields
- `id` (INTEGER, PRIMARY KEY, AUTO_INCREMENT)
- `description` (TEXT, NOT NULL) - Task description text
- `completed` (BOOLEAN, DEFAULT FALSE) - Whether task is completed
- `user_id` (INTEGER, FOREIGN KEY, NOT NULL) - Owner of the task
- `priority` (ENUM: 'HIGH', 'MEDIUM', 'LOW', DEFAULT 'MEDIUM') - Task priority level
- `tags` (JSON, DEFAULT []) - Array of tag strings for categorization
- `due_date` (TIMESTAMP, NULL) - Deadline for the task
- `recurrence_type` (ENUM: 'NONE', 'DAILY', 'WEEKLY', 'MONTHLY', DEFAULT 'NONE') - Recurrence pattern
- `reminder_time` (INTEGER, DEFAULT 10) - Minutes before due time for notification
- `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP) - Creation time
- `updated_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP) - Last update time

### Relationships
- `user_id` → `users.id` (Many-to-One relationship)

### Validation Rules
- `priority` must be one of: 'HIGH', 'MEDIUM', 'LOW'
- `recurrence_type` must be one of: 'NONE', 'DAILY', 'WEEKLY', 'MONTHLY'
- `reminder_time` must be >= 0
- `due_date` must be a valid future date if provided
- `tags` must be an array of strings if provided
- `description` length between 1 and 500 characters
- `user_id` must reference an existing user

### State Transitions
- `completed` can transition from FALSE to TRUE or TRUE to FALSE
- `priority` can be updated at any time
- `due_date` can be updated at any time
- `recurrence_type` can be changed at any time

## Entity: User (Unchanged)
- No changes to User entity required - all new features are task-specific

## Indexes
- `idx_user_priority` on (user_id, priority) for priority filtering
- `idx_user_due_date` on (user_id, due_date) for due date filtering
- `idx_user_created_at` on (user_id, created_at) for chronological sorting
- `idx_user_completed` on (user_id, completed) for status filtering
- `idx_user_priority_due_date` on (user_id, priority, due_date) for combined filtering