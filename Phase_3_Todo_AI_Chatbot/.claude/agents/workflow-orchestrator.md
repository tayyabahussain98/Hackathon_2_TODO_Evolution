# Phase-3 Todo AI Chatbot Workflow Orchestrator

## Overview
This document describes the workflow orchestrator for the Phase-3 Todo AI Chatbot system. It defines how the various agents and skills work together to create a cohesive AI-powered todo management system.

## System Architecture

### Core Components
- **chatbot-ui-agent**: Handles OpenAI ChatKit UI integration, chat components, message bubbles, input field, and layout in frontend
- **mcp-tool-agent**: Designs and implements stateless MCP tools for todo operations (add_task, list_tasks, complete_task, delete_task, update_task)
- **openrouter-agent**: Manages OpenAI Agents SDK runner with OpenRouter API key, prompt crafting, tool calling, and agent logic
- **conversation-agent**: Handles conversation and message models, persistence in Neon DB, SQLModel CRUD for conversations and messages
- **chat-endpoint-agent**: Implements FastAPI POST /api/chat endpoint, stateless logic, conversation loading/saving, agent invocation

### Supporting Skills
- **chatkit-ui**: Prompt for integrating OpenAI ChatKit UI, message rendering, input handling, and styling with ShadCN
- **mcp-tool-design**: Prompt for creating stateless MCP tools with parameters, returns, and examples for todo operations
- **openrouter-integration**: Prompt for configuring OpenAI Agents SDK with OpenRouter API key, base_url, and headers
- **db-conversation**: Prompt for defining SQLModel Conversation and Message models, CRUD operations, and Alembic migration
- **agent-behavior**: Prompt for defining agent behavior, natural language parsing, tool selection, and response formatting

## Workflow Orchestration

### 1. Initialization Workflow
1. **openrouter-agent** initializes the OpenAI Agents SDK with OpenRouter configuration
2. **conversation-agent** sets up database connections and initializes SQLModel models
3. **mcp-tool-agent** creates stateless MCP tools for todo operations
4. **chat-endpoint-agent** establishes the API endpoint infrastructure
5. **chatbot-ui-agent** sets up the frontend UI components

### 2. User Interaction Workflow
1. User sends a message through the **chatbot-ui-agent**
2. **chat-endpoint-agent** receives the POST /api/chat request
3. **conversation-agent** loads or creates a conversation record
4. **openrouter-agent** processes the message with the AI agent
5. **agent-behavior** determines the appropriate response and tool selection
6. If todo operations are needed:
   - **mcp-tool-agent** executes the appropriate todo operation
   - Updated tasks are persisted by **conversation-agent**
7. Response is formatted and sent back through **chatbot-ui-agent**

### 3. Todo Operations Workflow
#### Add Task
1. Natural language parsing identifies "add task" intent via **agent-behavior**
2. **mcp-tool-agent** executes `add_task` operation
3. **conversation-agent** persists the new task to Neon DB
4. Confirmation message is generated and returned

#### List Tasks
1. Natural language parsing identifies "list tasks" intent via **agent-behavior**
2. **mcp-tool-agent** executes `list_tasks` operation
3. **conversation-agent** retrieves tasks from Neon DB
4. Formatted task list is returned to user

#### Complete Task
1. Natural language parsing identifies "complete task" intent via **agent-behavior**
2. **mcp-tool-agent** executes `complete_task` operation
3. **conversation-agent** updates task status in Neon DB
4. Confirmation message is generated and returned

#### Delete Task
1. Natural language parsing identifies "delete task" intent via **agent-behavior**
2. **mcp-tool-agent** executes `delete_task` operation
3. **conversation-agent** removes task from Neon DB
4. Confirmation message is generated and returned

#### Update Task
1. Natural language parsing identifies "update task" intent via **agent-behavior**
2. **mcp-tool-agent** executes `update_task` operation
3. **conversation-agent** updates task details in Neon DB
4. Confirmation message is generated and returned

## Agent Coordination

### Data Flow Between Agents
```
UI Input → chatbot-ui-agent → chat-endpoint-agent → conversation-agent → openrouter-agent → agent-behavior → mcp-tool-agent → conversation-agent → Response Generation → chatbot-ui-agent → UI Output
```

### Error Handling Strategy
- **openrouter-agent** handles API connectivity issues
- **mcp-tool-agent** validates input parameters before executing operations
- **conversation-agent** manages database transaction errors
- **chat-endpoint-agent** provides appropriate HTTP status codes
- **chatbot-ui-agent** displays user-friendly error messages

### State Management
- Conversations are managed by **conversation-agent** in Neon DB
- UI state is maintained by **chatbot-ui-agent**
- Agent state is handled by **openrouter-agent** and **agent-behavior**
- Task state is managed by **mcp-tool-agent** and persisted by **conversation-agent**

## Configuration and Setup

### Environment Variables
- OPENROUTER_API_KEY: API key for OpenRouter
- NEON_DB_URL: Connection string for Neon DB
- FRONTEND_BASE_URL: Base URL for the frontend application

### MCP Tool Specifications
Each MCP tool follows these patterns:
- Stateless operation
- Proper parameter validation
- Consistent return format
- Error handling and logging

## Implementation Guidelines

### Using the Skills
1. **chatkit-ui**: Follow the guidelines for UI component implementation
2. **mcp-tool-design**: Adhere to the tool design patterns for consistency
3. **openrouter-integration**: Use the configuration patterns for API setup
4. **db-conversation**: Implement models and CRUD operations as specified
5. **agent-behavior**: Apply the behavior patterns for natural language processing

### Best Practices
- Maintain separation of concerns between agents
- Use consistent error handling patterns
- Implement proper logging and monitoring
- Follow security best practices for API keys and user data
- Ensure responsive UI experiences

## Testing Strategy
- Unit tests for individual agents
- Integration tests for agent coordination
- End-to-end tests for complete workflows
- Load testing for API endpoints
- UI testing for frontend components

## Monitoring and Observability
- Log important events from each agent
- Monitor API response times and error rates
- Track user interaction patterns
- Monitor database performance
- Set up alerts for critical failures