---
description: Debug CopilotKit integration issues (state sync, streaming, interrupts)
---

Debug CopilotKit-related issues in the BLOG-CANVAS-COPILOTkit project.

## Debugging Workflow

### Step 1: Identify the Issue
Ask the user about the problem:
- State not syncing between agent and frontend?
- Streaming content not working?
- Interrupts not triggering?
- CoAgent not responding?
- Type mismatches?
- Performance issues?

### Step 2: Gather Information

Run diagnostic checks:

**Check Agent Status:**
```bash
cd agent
langgraph status  # or check http://localhost:8123
```

**Check Frontend Console:**
- Open browser DevTools
- Check for CopilotKit errors
- Verify state updates in React DevTools

**Check Logs:**
- Agent logs from LangGraph server
- Frontend console logs
- Network tab for API calls

### Step 3: Common Issues & Solutions

#### Issue: State Not Syncing

**Symptoms:**
- Frontend doesn't receive state updates
- State shows as undefined/null
- Stale state in UI

**Debug Steps:**
1. Verify `copilotkit_emit_state()` is called in agent
2. Check state schema matches between Python and TypeScript
3. Verify CopilotKitProvider is properly configured
4. Check network requests in DevTools

**Common Fixes:**
```python
# Ensure state emission after updates
await copilotkit_emit_state(state)
```

```typescript
// Verify provider setup
<CopilotKit runtimeUrl="/api/copilotkit">
  {children}
</CopilotKit>
```

#### Issue: Streaming Not Working

**Symptoms:**
- Content doesn't update in real-time
- Loading indicators stuck
- Partial content not showing

**Debug Steps:**
1. Check if agent emits intermediate states
2. Verify streaming hook setup
3. Check for proper state key paths
4. Verify generator functions are async

**Common Fixes:**
```python
# Emit state during processing, not just at the end
for item in items:
    state["current_item"] = item
    await copilotkit_emit_state(state)
    process(item)
```

```typescript
// Ensure streaming hook is properly configured
const { content } = useStreamingContent({
  stateKey: "sections",
  contentKey: "content"
});
```

#### Issue: Interrupts Not Triggering

**Symptoms:**
- Agent doesn't wait for user approval
- Review UI doesn't appear
- Workflow skips approval step

**Debug Steps:**
1. Verify `interrupt()` is called in agent
2. Check interrupt identifier is unique
3. Verify frontend has approval UI
4. Check if checkpoint is properly configured

**Common Fixes:**
```python
# Ensure interrupt is properly called
async def review_node(state):
    await copilotkit_emit_state(state)
    interrupt("awaiting_approval")  # Must be called
    return state
```

```typescript
// Ensure UI handles the interrupt state
useCoAgentStateRender({
  name: "research_agent",
  render: ({ state }) => {
    if (state.proposal && !state.outline) {
      return <ProposalViewer />;
    }
    return null;
  }
});
```

#### Issue: Type Mismatches

**Symptoms:**
- TypeScript errors in frontend
- Python validation errors
- Data shape inconsistencies

**Debug Steps:**
1. Compare state definitions (state.py vs types.ts)
2. Check for missing fields or wrong types
3. Verify JSON serialization/deserialization
4. Check for optional vs required fields

**Common Fixes:**
```python
# state.py - Ensure proper typing
class ResearchState(CopilotKitState):
    title: str = ""  # Default value
    sections: list[dict] = []  # Proper list type
```

```typescript
// types.ts - Match Python schema
interface ResearchState {
  title: string;
  sections: Array<{/* ... */}>;
}
```

#### Issue: CoAgent Not Responding

**Symptoms:**
- Chat messages don't trigger agent
- No response from backend
- Timeout errors

**Debug Steps:**
1. Check agent server is running (port 8123)
2. Verify tunnel is active
3. Check API route configuration
4. Verify API keys are set
5. Check for agent errors in logs

**Common Fixes:**
```bash
# Restart agent server
cd agent
langgraph up

# Restart tunnel in new terminal
npx copilotkit@latest dev --port 8123
```

```typescript
// Verify API route
// frontend/src/app/api/copilotkit/route.ts
export const POST = async (req: Request) => {
  return new CopilotRuntime({
    url: process.env.AGENT_URL || "http://localhost:8123"
  }).response(req);
};
```

### Step 4: Advanced Debugging

#### Enable Verbose Logging

**Agent:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Frontend:**
```typescript
// Add console.log in useEffect
useEffect(() => {
  console.log("State updated:", state);
}, [state]);
```

#### Check LangSmith Traces
1. Open LangSmith dashboard
2. Find the trace for your request
3. Examine each node execution
4. Check input/output at each step

#### Network Analysis
1. Open DevTools Network tab
2. Filter by "copilotkit"
3. Examine request/response payloads
4. Check for errors or timeouts

### Step 5: Performance Issues

If experiencing slowness:
1. Check token usage in LangSmith
2. Verify streaming is enabled
3. Check for unnecessary state emissions
4. Optimize tool execution
5. Consider caching strategies

### Verification Checklist

After fixing, verify:
- [ ] State syncs correctly
- [ ] Streaming works smoothly
- [ ] Interrupts trigger appropriately
- [ ] No console errors
- [ ] Types are consistent
- [ ] Performance is acceptable
- [ ] Error handling works

## Quick Diagnostic Commands

```bash
# Check agent health
curl http://localhost:8123/health

# Check running processes
ps aux | grep langgraph
ps aux | grep copilotkit

# Check environment variables
cd frontend && cat .env
cd agent && cat .env
```

**What CopilotKit issue are you experiencing?**
