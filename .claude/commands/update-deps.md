---
description: Update project dependencies (frontend and agent)
---

Update dependencies for both frontend and agent, safely and systematically.

## Dependency Update Process:

### Frontend Dependencies:

1. **Check current versions**:
   - Navigate to `frontend/`
   - Show current package.json versions for major packages:
     - Next.js
     - React
     - CopilotKit packages
     - TypeScript
     - Tailwind CSS

2. **Check for updates**:
   - Run `pnpm outdated` to see available updates
   - Highlight major vs minor vs patch updates

3. **Update strategy**:
   - **Patch updates**: Generally safe, run `pnpm update`
   - **Minor updates**: Review changelogs, update selectively
   - **Major updates**: Careful review required, especially for:
     - Next.js (check migration guides)
     - React (breaking changes)
     - CopilotKit (API changes)

4. **Update process**:
   - Create backup of package.json and pnpm-lock.yaml
   - Update packages
   - Run `pnpm install`
   - Test build: `pnpm run build`
   - Test dev server: `pnpm run dev`

### Agent Dependencies:

1. **Check current versions**:
   - Navigate to `agent/`
   - Show current requirements.txt versions for major packages:
     - langchain
     - langgraph
     - copilotkit
     - tavily-python
     - langchain-openai

2. **Check for updates**:
   - Run `pip list --outdated` for packages in requirements.txt

3. **Update strategy**:
   - **Pin versions**: Note that langgraph-cli is pinned (0.1.71)
   - **langchain-core**: Note version constraint (~=0.3.15)
   - **Major updates**: Review changelogs for breaking changes

4. **Update process**:
   - Create backup of requirements.txt
   - Update versions in requirements.txt
   - Run `pip install -r requirements.txt`
   - Test agent: `langgraph up`

### Post-Update Verification:

- [ ] Frontend builds without errors
- [ ] Frontend dev server starts
- [ ] Agent starts successfully
- [ ] Full workflow works (search → outline → approve → write)
- [ ] No console/log errors
- [ ] CopilotKit integration still works

Provide a summary of what was updated and any breaking changes to watch for.
