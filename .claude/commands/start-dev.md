---
description: Start the complete development environment (agent + frontend + tunnel)
---

Start the complete development environment for the BLOG-CANVAS-COPILOTkit project.

## Steps:

1. **Check environment files**:
   - Verify `agent/.env` exists with required keys (OPENAI_API_KEY, TAVILY_API_KEY, LANGSMITH_API_KEY)
   - Verify `frontend/.env` exists with required keys (OPENAI_API_KEY, LANGSMITH_API_KEY, NEXT_PUBLIC_COPILOT_CLOUD_API_KEY)
   - If missing, list what's needed

2. **Start the LangGraph agent**:
   - Navigate to `agent/`
   - Run `langgraph up` in background
   - Note the agent URL (typically http://localhost:8123)
   - Wait for successful startup confirmation

3. **Create tunnel to agent**:
   - Run `npx copilotkit@latest dev --port 8123` in background
   - Note the tunnel URL

4. **Install frontend dependencies** (if needed):
   - Navigate to `frontend/`
   - Run `pnpm install` if node_modules is missing or package.json changed

5. **Start frontend**:
   - Navigate to `frontend/`
   - Run `pnpm run dev` in background
   - Note the frontend URL (typically http://localhost:3000)

6. **Provide summary**:
   - List all running services with their URLs
   - Provide instructions to access the app
   - Note any errors encountered

IMPORTANT: Run services in background so user can continue working. Monitor output for errors.
