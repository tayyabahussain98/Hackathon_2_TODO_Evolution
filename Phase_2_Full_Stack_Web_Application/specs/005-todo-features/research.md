# Research: Enhanced Todo Features

## Overview
Research for implementing intermediate and advanced features for the todo application including priorities, tags, search & filter, sort, due dates, recurring tasks, and browser notifications.

## Database Schema Decisions

### Decision: Priority Field Implementation
- **Rationale**: Using ENUM field for priority levels (HIGH, MEDIUM, LOW) provides type safety and efficient storage
- **Alternatives considered**: String field with validation, separate priority table
- **Chosen approach**: ENUM field in todos table for simplicity and performance

### Decision: Tags Field Implementation
- **Rationale**: Using JSON field to store array of tags allows flexible tagging with efficient querying
- **Alternatives considered**: Separate tags table with many-to-many relationship, comma-separated string
- **Chosen approach**: JSON field in todos table for simplicity and to avoid complex joins

### Decision: Due Date Field Implementation
- **Rationale**: TIMESTAMP field allows precise date/time storage with timezone support
- **Alternatives considered**: DATE only, string field with validation
- **Chosen approach**: TIMESTAMP field for full date/time precision

### Decision: Recurrence Field Implementation
- **Rationale**: ENUM field for recurrence patterns (NONE, DAILY, WEEKLY, MONTHLY) provides clear options
- **Alternatives considered**: String field with validation, separate recurrence configuration table
- **Chosen approach**: ENUM field for simplicity and type safety

## Backend Technology Decisions

### Decision: Search Implementation
- **Rationale**: Using database-level text search with full-text indexing for performance
- **Alternatives considered**: Application-level filtering, separate search service
- **Chosen approach**: Database-level search with proper indexing for efficiency

### Decision: Filtering and Sorting Implementation
- **Rationale**: Implementing in service layer with database queries for optimal performance
- **Alternatives considered**: Client-side filtering/sorting, separate service
- **Chosen approach**: Server-side implementation with database optimization

## Frontend Technology Decisions

### Decision: Priority Selection Component
- **Rationale**: Using ShadCN Select component for consistent UI and accessibility
- **Alternatives considered**: Radio buttons, custom dropdown
- **Chosen approach**: ShadCN Select for consistency with existing UI

### Decision: Tags Input Component
- **Rationale**: Using ShadCN Combobox or custom tag input for multi-tag selection
- **Alternatives considered**: Multiple checkboxes, separate tag management
- **Chosen approach**: Multi-select input component for ease of use

### Decision: Date Picker Component
- **Rationale**: Using ShadCN DatePicker for consistent UI and accessibility
- **Alternatives considered**: Native HTML input, custom date picker
- **Chosen approach**: ShadCN DatePicker for consistency with design system

### Decision: Browser Notifications
- **Rationale**: Using Web Notifications API for native browser notifications
- **Alternatives considered**: In-app notifications, toast messages
- **Chosen approach**: Browser notifications for external reminders

## Performance Considerations

### Decision: Indexing Strategy
- **Rationale**: Proper indexing on frequently queried fields (priority, due_date, user_id) for performance
- **Implementation**: Composite indexes for combined queries, single-column indexes for individual filters

### Decision: Client-side vs Server-side Operations
- **Rationale**: Server-side filtering/sorting for large datasets, client-side for small datasets
- **Implementation**: Primary filtering/sorting at server, client-side caching for responsiveness

## Security Considerations

### Decision: User Data Isolation
- **Rationale**: All new features must maintain user-specific data isolation
- **Implementation**: All queries continue to filter by user_id to maintain privacy

### Decision: Input Validation
- **Rationale**: Proper validation of all new fields to prevent injection and ensure data quality
- **Implementation**: Backend validation at API layer, frontend validation for UX