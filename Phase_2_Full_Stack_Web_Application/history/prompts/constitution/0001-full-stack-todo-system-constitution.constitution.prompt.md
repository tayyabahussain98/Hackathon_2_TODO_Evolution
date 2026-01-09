---
id: 0001
title: Full-Stack Todo System Constitution
stage: constitution
date: 2025-12-28
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: win
command: /sp.constitution
labels: ["constitution", "architecture", "full-stack", "workflow", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

# Full-Stack Todo System
## 🎯 Goal

Upgrade the CLI Todo app into a modular, reusable full-stack system with:

clear separation of layers

reusable code

organized agents + skills

scalable structure

No mixing layers.
No coding without planning.
No shortcuts.

## 🔁 Required Workflow
Specify → Plan → Tasks → Implement → Review


❌ No coding before specification
❌ No skipping planning
❌ No mixing folders
❌ No "temporary hacks"

## 🏗 Monorepo Structure
project/
│
├── specs/
│
├── agents/
│   ├── backend/
│   │   ├── backend-agent
│   │   ├── api-routes-agent
│   │   ├── services-agent
│   │   ├── middleware-agent
│   │   └── skills/
│   │       ├── backend-planning
│   │       ├── api-implementation
│   │       └── service-design
│   │
│   ├── frontend/
│   │   ├── frontend-agent
│   │   ├── ui-components-agent
│   │   ├── pages-agent
│   │   └── skills/
│   │       ├── ui-layout
│   │       └── api-client-handling
│   │
│   ├── auth/
│   │   ├── auth-agent
│   │   ├── jwt-agent
│   │   ├── oauth-agent
│   │   └── skills/
│   │       ├── auth-planning
│   │       ├── jwt-verification
│   │       └── google-oauth-prep
│   │
│   └── database/
│       ├── database-agent
│       ├── schema-agent
│       ├── migration-agent
│       └── skills/
│           ├── schema-modeling
│           └── migration-planning
│
├── backend/
│   └── app/
│       ├── main.py
│       ├── routes/
│       ├── services/
│       ├── models/
│       ├── middleware/
│       └── core/
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── auth-ui/
│
├── auth/
│   ├── config/
│   ├── tokens/
│   ├── providers/
│   └── docs/
│
├── database/
│   ├── schema/
│   ├── migrations/
│   └── seeds/
│
└── shared/
    ├── utils/
    ├── constants/
    └── types/

# 🎨 Architecture Rules
## 🟥 Backend

routes = API only

services = business logic

models = data contracts

middleware = auth/security

❌ No UI
❌ No SQL in routes

## 🟦 Frontend (CLI or Web)

components reusable

logic separated

backend calls only via /lib/api

❌ No DB access
❌ No business logic inside components

## 🟡 Authentication (Google-ready)

JWT sessions

Google OAuth planned

secrets never hard-coded

Reusable across apps.

## 🟢 Database

schema controlled

migrations tracked

never modify DB manually

# 🧩 Task Definition

Every task must include:

Task ID
Purpose
Files involved
Acceptance criteria
Out-of-scope
Validation checklist


➡️ No task = No code.

# ✍ Implementation Rules

implement only assigned task

readable + testable

respect folder boundaries

reuse helpers — no duplication

# 🔍 Review Checklist

Approve only if:

matches spec

follows architecture

stays inside correct folder

adds nothing extra

easy to understand

Otherwise → fix.

## Response snapshot

Created Full-Stack Todo System Constitution v1.0.0 with 8 core principles:

1. **Spec-Driven Workflow (NON-NEGOTIABLE)**: Enforce Specify → Plan → Tasks → Implement → Review with no shortcuts
2. **Layer Separation**: Strict boundaries between Backend, Frontend, Auth, and Database layers
3. **Backend Architecture**: Clean architecture with routes/services/models/middleware separation
4. **Frontend Architecture**: Component-based with centralized API communication via lib/api.ts
5. **Authentication Architecture**: JWT + Better Auth with Google OAuth planned, no hardcoded secrets
6. **Database Architecture**: Migration-driven schema management with SQLModel
7. **Monorepo Structure**: Domain-separated folders with agents/{domain} and code in {domain}/
8. **Task Definition Standard**: Every task requires ID, purpose, files, criteria, scope, checklist

Added Implementation Standards, Review Standards, and Governance sections with clear approval/rejection criteria.

Version 1.0.0 ratified 2025-12-28. Templates flagged for review to ensure alignment with new principles.

## Outcome

- ✅ Impact: Created foundational constitution establishing architectural principles and workflow enforcement for Full-Stack Todo System
- 🧪 Tests: No tests (documentation artifact)
- 📁 Files: Created .specify/memory/constitution.md (version 1.0.0)
- 🔁 Next prompts: Review and update template files (plan-template.md, spec-template.md, tasks-template.md) for consistency with constitution principles
- 🧠 Reflection: Constitution provides clear, enforceable rules for layer separation, workflow discipline, and code review standards. Strong foundation for preventing technical debt and maintaining architectural integrity.

## Evaluation notes (flywheel)

- Failure modes observed: None (initial constitution creation)
- Graders run and results (PASS/FAIL): N/A (documentation artifact)
- Prompt variant (if applicable): N/A (initial creation)
- Next experiment (smallest change to try): Test constitution enforcement by creating a feature spec and verifying workflow compliance
