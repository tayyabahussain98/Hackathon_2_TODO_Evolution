<!-- SYNC IMPACT REPORT:
Version change: N/A -> 1.0.0
Added sections: AI Todo Chatbot specific principles
Removed sections: None
Modified principles: N/A (new constitution)
Templates requiring updates: ⚠ pending - plan-template.md, spec-template.md, tasks-template.md
Follow-up TODOs: None
-->
# AI Todo Chatbot Constitution

## Core Principles

### I. No Manual Coding Rule
No manual coding. Only AI-generated code allowed. All implementations must follow the strict pipeline of Specification → Planning → Tasks → Implementation → Review. No shortcuts, no guessing, no architecture drift.

### II. Technology Stack Compliance
Mandatory use of specified technology stack: OpenAI ChatKit for frontend, FastAPI for backend, OpenAI Agents SDK with OpenRouter, SQLModel ORM, Neon Serverless PostgreSQL, and existing authentication system. Deviations require explicit constitutional amendment.

### III. Architecture Preservation
Extend existing codebase without overwriting or removing existing todo/auth functionality. Maintain backward compatibility while adding new AI-powered features. All new components must integrate seamlessly with existing architecture.

### IV. Statelessness Requirement
All MCP tools and API endpoints must be stateless. Conversation state persisted in DB (conversations, messages tables). No session-based or in-memory state management for core functionality.

### V. MCP Tool Standardization
MCP server exposes only stateless tools: add_task, list_tasks, complete_task, delete_task, update_task. All tools must be user-specific using user_id from JWT for security and isolation.

### VI. Natural Language Processing
Core feature: Natural language todo control allowing users to interact with the system using conversational language. Agent must confirm actions with user-friendly responses.

## Additional Constraints

### Database Requirements
- conversations table: user_id (FK), id, created_at, updated_at
- messages table: user_id (FK), conversation_id (FK), role (user/assistant), content, created_at
- Use Alembic for migrations
- Maintain referential integrity and proper indexing

### Security & Authentication
- Validate user_id from JWT in all operations
- Never expose API keys in client-side code
- Use OPENROUTER_API_KEY only from .env
- All operations must be user-isolated using JWT authentication

### Quality Standards
- Type hints, docstrings, PEP 8 compliance
- Graceful error handling in agent responses
- Proper logging and monitoring
- Comprehensive test coverage for all new functionality

## Development Workflow

### Pipeline Enforcement
- Strict adherence to Specify → Plan → Tasks → Implement → Review pipeline
- Every change must have Task ID for traceability
- MCP tools must be stateless and follow SDK specifications
- Agent must confirm actions ("Task added: Buy milk")

### API Integration
- Use OpenRouter base_url and API key in AsyncOpenAI client (https://openrouter.ai/api/v1)
- Support multiple OpenRouter models (gpt-4o-mini, claude-3.5-sonnet, gemini-1.5-flash)
- Implement proper rate limiting and error handling

### Frontend Integration
- OpenAI ChatKit integration for chatbot UI
- New page (/chatbot) or integration with existing UI
- Responsive design and accessibility compliance
- Real-time conversation updates

## Governance

### Amendment Procedure
Changes to this constitution require formal amendment process with justification, impact assessment, and approval from project maintainers. All amendments must be backward compatible unless explicitly stated otherwise.

### Versioning Policy
- MAJOR: Backward incompatible governance/principle removals or redefinitions
- MINOR: New principle/section added or materially expanded guidance
- PATCH: Clarifications, wording, typo fixes, non-semantic refinements

### Compliance Review
All pull requests must verify compliance with constitutional principles. Automated checks should validate:
- Technology stack adherence
- Architecture preservation
- Security requirements
- Code generation rules

**Version**: 1.0.0 | **Ratified**: 2026-01-15 | **Last Amended**: 2026-01-15