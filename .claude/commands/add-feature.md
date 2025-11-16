---
description: Guide for adding a new feature to the application
---

Guide the user through adding a new feature to BLOG-CANVAS-COPILOTkit.

## Feature Addition Workflow:

Ask the user to describe the feature they want to add. Then, based on the feature type, follow the appropriate path:

### For Frontend Features (UI/UX):

1. **Analyze requirements**:
   - Determine which components need changes
   - Identify new components needed
   - Consider state management implications

2. **Implementation plan**:
   - Create/modify components in `frontend/src/components/`
   - Update types in `frontend/src/lib/types/`
   - Add any new hooks in `frontend/src/lib/hooks/`
   - Update routing in `frontend/src/app/` if needed

3. **Integration**:
   - Integrate with CopilotKit hooks if AI-related
   - Update context providers if state changes
   - Add shadcn/ui components if needed

### For Agent Features (Backend/AI):

1. **Analyze requirements**:
   - Determine if new tools are needed
   - Consider state schema changes
   - Plan LangGraph workflow modifications

2. **Implementation plan**:
   - Add new tools in `agent/tools/`
   - Update `agent/state.py` if state changes
   - Modify `agent/graph.py` for new nodes/edges
   - Update system prompt in `agent/graph.py`

3. **Integration**:
   - Register new tools in ResearchAgent
   - Update CopilotKit state emission
   - Add corresponding frontend handling

### For Full-Stack Features:

Follow both Frontend and Agent paths, ensuring:
- State synchronization between agent and frontend
- Type consistency across TypeScript and Python
- Proper error handling on both sides

### Testing Checklist:

- [ ] Feature works in local development
- [ ] No console errors in frontend
- [ ] Agent logs show expected behavior
- [ ] State updates correctly
- [ ] UI is responsive and accessible
- [ ] Error cases are handled

After implementation, ask if the user wants to:
- Add tests
- Update documentation (CLAUDE.md)
- Create a custom slash command for this feature
