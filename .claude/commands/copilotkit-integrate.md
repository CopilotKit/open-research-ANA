---
description: Guide for integrating CopilotKit features into the project
---

Help the user integrate a new CopilotKit feature into the BLOG-CANVAS-COPILOTkit project.

## Integration Workflow

### Step 1: Understand the Feature
Ask the user what they want to integrate:
- New CoAgent functionality?
- Additional hooks or actions?
- AG-UI components?
- State management enhancement?
- New streaming pattern?

### Step 2: Analyze Current Architecture
Review the existing implementation:
- Check `frontend/src/app/api/copilotkit/route.ts`
- Review agent state in `agent/state.py`
- Examine existing hooks in `frontend/src/lib/hooks/`
- Check current CoAgent setup

### Step 3: Plan the Integration

#### For Frontend Features:
1. Identify which components need updates
2. Determine new hooks needed
3. Plan state synchronization
4. Consider UX/UI implications

#### For Agent Features:
1. Determine if new tools are needed
2. Plan state schema changes
3. Design LangGraph workflow modifications
4. Consider interrupt/approval patterns

#### For Full-Stack Features:
1. Design state schema (Python + TypeScript)
2. Plan backend tools and nodes
3. Design frontend UI and hooks
4. Ensure bidirectional sync

### Step 4: Implementation Checklist

**Backend (`/agent`):**
- [ ] Update `state.py` with new state fields
- [ ] Create new tools in `tools/` if needed
- [ ] Modify `graph.py` for new nodes/edges
- [ ] Add `copilotkit_emit_state()` calls
- [ ] Update system prompts if needed

**Frontend (`/frontend`):**
- [ ] Update types in `src/lib/types/`
- [ ] Create/modify components in `src/components/`
- [ ] Add hooks in `src/lib/hooks/`
- [ ] Update CopilotKit provider if needed
- [ ] Add UI for new features

**Integration:**
- [ ] Test state synchronization
- [ ] Verify streaming works
- [ ] Test error handling
- [ ] Check interrupt patterns (if applicable)
- [ ] Update documentation

### Step 5: Testing

1. Start the agent: `cd agent && langgraph up`
2. Start the tunnel: `npx copilotkit@latest dev --port 8123`
3. Start frontend: `cd frontend && pnpm dev`
4. Test the feature end-to-end

### CopilotKit Integration Patterns

#### Adding a New Action
```typescript
// Frontend
useCopilotAction({
  name: "my_action",
  description: "Action description",
  parameters: [/* ... */],
  handler: async ({ param }) => {
    // Handle action
  }
});
```

#### Adding a New Tool (Agent)
```python
# Backend
@tool
async def my_tool(query: str) -> str:
    """Tool description."""
    result = await perform_action(query)
    await copilotkit_emit_state({"status": "updated"})
    return result
```

#### Adding State Synchronization
```python
# state.py
class ResearchState(CopilotKitState):
    my_new_field: str = ""
```

```typescript
// types.ts
interface ResearchState {
  myNewField: string;
}
```

### Common Integrations

1. **Add a new approval workflow**: Use interrupt + useCoAgentStateRender
2. **Add streaming content**: Use copilotkit_emit_state + useStreamingContent
3. **Add a new tool**: Create in agent/tools/, bind in graph.py
4. **Add AG-UI**: Create Pydantic models, integrate with CoAgent
5. **Add progress indicators**: Emit state logs, render in Progress component

### Best Practices

- Keep state schemas in sync (Python ↔ TypeScript)
- Always emit state after significant changes
- Use interrupts for user approval
- Provide clear progress indicators
- Handle errors gracefully on both sides
- Test state sync thoroughly

**What CopilotKit feature would you like to integrate?**
