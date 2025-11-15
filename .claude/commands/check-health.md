---
description: Check health status of all services (agent, frontend, APIs)
---

Perform a comprehensive health check of the BLOG-CANVAS-COPILOTkit application.

## Health Checks:

1. **Agent Service**:
   - Check if langgraph process is running
   - Test connectivity to http://localhost:8123 (or configured port)
   - Verify agent responds to health check

2. **Frontend Service**:
   - Check if Next.js dev server is running
   - Test connectivity to http://localhost:3000 (or configured port)
   - Verify frontend can reach backend

3. **Environment Configuration**:
   - Verify agent/.env has all required keys:
     - OPENAI_API_KEY
     - TAVILY_API_KEY
     - LANGSMITH_API_KEY
   - Verify frontend/.env has all required keys:
     - OPENAI_API_KEY
     - LANGSMITH_API_KEY
     - NEXT_PUBLIC_COPILOT_CLOUD_API_KEY
   - Check for any missing or placeholder values

4. **Dependencies**:
   - Check if `frontend/node_modules` exists
   - Check if `agent/` has required Python packages installed
   - List any missing dependencies

5. **API Connectivity** (if possible):
   - Test OpenAI API key validity (optional)
   - Test Tavily API key validity (optional)
   - Note: Only test if we can do so without making expensive calls

6. **Port Availability**:
   - Check if ports 8123 (agent), 3000 (frontend) are in use
   - Identify what's using them

Provide a summary report with:
- ✅ Green checks for healthy services
- ⚠️ Warnings for potential issues
- ❌ Red flags for critical problems
- Actionable recommendations to fix issues
