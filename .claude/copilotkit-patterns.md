# CopilotKit Patterns & Best Practices

A comprehensive guide to common CopilotKit patterns and best practices for building CoAgents with human-in-the-loop workflows.

## Table of Contents

1. [Core Patterns](#core-patterns)
2. [State Management](#state-management)
3. [Streaming Patterns](#streaming-patterns)
4. [Human-in-the-Loop](#human-in-the-loop)
5. [Framework Integrations](#framework-integrations)
6. [AG-UI Patterns](#ag-ui-patterns)
7. [Performance Optimization](#performance-optimization)
8. [Error Handling](#error-handling)

---

## Core Patterns

### 1. Basic CoAgent Setup

#### Backend (LangGraph + CopilotKit)

```python
# state.py
from copilotkit import CopilotKitState
from typing import Annotated
from langgraph.graph import StateGraph, MessagesState

class MyAgentState(CopilotKitState, MessagesState):
    """Agent state with CopilotKit integration."""
    title: str = ""
    content: str = ""
    status: str = "idle"

# graph.py
from langgraph.graph import StateGraph, END
from copilotkit import copilotkit_emit_state, copilotkit_exit

async def process_node(state: MyAgentState):
    """Process node with state emission."""
    # Do work
    state["status"] = "processing"
    await copilotkit_emit_state(state)

    # More work
    result = await perform_task(state)
    state["content"] = result
    state["status"] = "complete"

    await copilotkit_emit_state(state)
    return state

# Build graph
graph = StateGraph(MyAgentState)
graph.add_node("process", process_node)
graph.set_entry_point("process")
graph.add_edge("process", END)

agent = graph.compile()
```

#### Frontend (React + CopilotKit)

```typescript
// app/layout.tsx
import { CopilotKit } from "@copilotkit/react-core";

export default function RootLayout({ children }) {
  return (
    <CopilotKit runtimeUrl="/api/copilotkit">
      {children}
    </CopilotKit>
  );
}

// app/api/copilotkit/route.ts
import { CopilotRuntime, LangGraphAgent } from "@copilotkit/runtime";

export const POST = async (req: Request) => {
  const runtime = new CopilotRuntime({
    agents: [
      new LangGraphAgent({
        name: "my_agent",
        url: process.env.AGENT_URL || "http://localhost:8123",
      }),
    ],
  });

  return runtime.response(req);
};

// components/MyComponent.tsx
import { useCoAgent, useCoAgentStateRender } from "@copilotkit/react-core";

export function MyComponent() {
  const { state, setState } = useCoAgent({
    name: "my_agent",
    initialState: {
      title: "",
      content: "",
      status: "idle",
    },
  });

  return (
    <div>
      <h1>{state.title}</h1>
      <p>{state.content}</p>
      <p>Status: {state.status}</p>
    </div>
  );
}
```

---

## State Management

### 1. Bidirectional State Sync

**Key Principle**: Keep state schemas in sync between Python and TypeScript.

#### Python State Schema

```python
from copilotkit import CopilotKitState
from typing import Optional, List
from pydantic import BaseModel

class Section(BaseModel):
    """Section model."""
    title: str
    content: str
    status: str = "pending"

class ResearchState(CopilotKitState):
    """Research state."""
    title: str = ""
    sections: List[Section] = []
    current_section: Optional[int] = None

    # Always emit after changes
    async def update_section(self, index: int, content: str):
        self.sections[index].content = content
        self.sections[index].status = "complete"
        await copilotkit_emit_state(self)
```

#### TypeScript State Schema

```typescript
// types.ts
interface Section {
  title: string;
  content: string;
  status: "pending" | "complete";
}

interface ResearchState {
  title: string;
  sections: Section[];
  currentSection: number | null;
}

// Use the schema
const { state } = useCoAgent<ResearchState>({
  name: "research_agent",
  initialState: {
    title: "",
    sections: [],
    currentSection: null,
  },
});
```

### 2. State Update Patterns

```python
# ✅ GOOD: Emit state after each significant update
async def write_section(state: ResearchState, index: int):
    state["sections"][index]["status"] = "writing"
    await copilotkit_emit_state(state)

    content = await generate_content()
    state["sections"][index]["content"] = content
    state["sections"][index]["status"] = "complete"
    await copilotkit_emit_state(state)

    return state

# ❌ BAD: Only emit at the end (no progress updates)
async def write_section_bad(state: ResearchState, index: int):
    state["sections"][index]["status"] = "writing"
    content = await generate_content()
    state["sections"][index]["content"] = content
    state["sections"][index]["status"] = "complete"
    await copilotkit_emit_state(state)  # Too late!
    return state
```

---

## Streaming Patterns

### 1. Streaming Content Generation

#### Backend: Emit State Incrementally

```python
async def generate_long_content(state: MyState):
    """Generate content with streaming updates."""
    state["content"] = ""
    state["status"] = "generating"
    await copilotkit_emit_state(state)

    chunks = []
    async for chunk in llm.astream(prompt):
        chunks.append(chunk)
        state["content"] = "".join(chunks)
        await copilotkit_emit_state(state)

    state["status"] = "complete"
    await copilotkit_emit_state(state)
    return state
```

#### Frontend: Use Streaming Hook

```typescript
import { useStreamingContent } from "@/lib/hooks/useStreamingContent";

export function ContentViewer() {
  const { content, isStreaming } = useStreamingContent({
    stateKey: "content",
    agentName: "my_agent",
  });

  return (
    <div>
      <div className="prose">{content}</div>
      {isStreaming && <LoadingIndicator />}
    </div>
  );
}
```

### 2. Progress Indicators

```python
# Backend: Emit logs for progress
async def multi_step_process(state: MyState):
    state["logs"] = []

    state["logs"].append({
        "message": "Starting research...",
        "level": "info"
    })
    await copilotkit_emit_state(state)

    # Step 1
    await step_one()
    state["logs"].append({
        "message": "Research complete. Analyzing results...",
        "level": "info"
    })
    await copilotkit_emit_state(state)

    # Step 2
    await step_two()
    state["logs"].append({
        "message": "Analysis complete!",
        "level": "success"
    })
    await copilotkit_emit_state(state)

    return state
```

```typescript
// Frontend: Render progress
import { useCoAgentStateRender } from "@copilotkit/react-core";

export function ProgressViewer() {
  useCoAgentStateRender({
    name: "my_agent",
    render: ({ state }) => (
      <div className="space-y-2">
        {state.logs?.map((log, i) => (
          <div key={i} className={`log-${log.level}`}>
            {log.message}
          </div>
        ))}
      </div>
    ),
  });

  return null;
}
```

---

## Human-in-the-Loop

### 1. Approval Workflow Pattern

#### Backend: Interrupt for Approval

```python
from langgraph.types import interrupt

async def propose_outline(state: ResearchState):
    """Generate outline and wait for approval."""
    # Generate proposal
    outline = await generate_outline(state["title"])
    state["proposal"] = outline
    state["status"] = "awaiting_approval"

    # Emit state so frontend can show proposal
    await copilotkit_emit_state(state)

    # Interrupt and wait for user feedback
    feedback = interrupt("outline_approval")

    # Process feedback
    if feedback.get("approved"):
        state["outline"] = state["proposal"]
        state["status"] = "approved"
    else:
        state["status"] = "rejected"
        state["feedback"] = feedback.get("comments", "")

    state["proposal"] = None
    await copilotkit_emit_state(state)
    return state
```

#### Frontend: Approval UI

```typescript
import { useCoAgentStateRender } from "@copilotkit/react-core";
import { useCopilotAction } from "@copilotkit/react-core";

export function ApprovalUI() {
  // Send approval back to agent
  useCopilotAction({
    name: "approve_outline",
    description: "Approve or reject the proposed outline",
    parameters: [
      {
        name: "approved",
        type: "boolean",
        description: "Whether the outline is approved",
      },
      {
        name: "comments",
        type: "string",
        description: "Feedback comments",
        required: false,
      },
    ],
    handler: async ({ approved, comments }) => {
      // This will resume the agent with the feedback
      return { approved, comments };
    },
  });

  // Render proposal when available
  useCoAgentStateRender({
    name: "research_agent",
    render: ({ state }) => {
      if (state.status === "awaiting_approval" && state.proposal) {
        return <ProposalViewer proposal={state.proposal} />;
      }
      return null;
    },
  });

  return null;
}

function ProposalViewer({ proposal }) {
  const [comments, setComments] = useState("");

  return (
    <div className="proposal-viewer">
      <h2>Outline Proposal</h2>
      <div className="outline">{/* Render outline */}</div>

      <textarea
        value={comments}
        onChange={(e) => setComments(e.target.value)}
        placeholder="Add feedback..."
      />

      <div className="actions">
        <button onClick={() => approveOutline(true, comments)}>
          Approve
        </button>
        <button onClick={() => approveOutline(false, comments)}>
          Reject
        </button>
      </div>
    </div>
  );
}
```

### 2. Conditional Approval Pattern

```python
async def selective_approval(state: MyState):
    """Approve individual items."""
    state["items_for_approval"] = generate_items()
    await copilotkit_emit_state(state)

    feedback = interrupt("item_approval")

    # User can approve specific items
    approved_items = [
        item for item in state["items_for_approval"]
        if item["id"] in feedback.get("approved_ids", [])
    ]

    state["approved_items"] = approved_items
    state["items_for_approval"] = []
    await copilotkit_emit_state(state)

    return state
```

---

## Framework Integrations

### 1. LangGraph + CopilotKit

```python
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from copilotkit import CopilotKitState, copilotkit_emit_state

class AgentState(CopilotKitState):
    current_step: str = ""
    result: str = ""

def create_graph():
    graph = StateGraph(AgentState)

    # Regular nodes
    graph.add_node("process", process_node)
    graph.add_node("tools", ToolNode(tools))

    # Routing
    def should_continue(state):
        if state.get("requires_tool"):
            return "tools"
        return END

    graph.set_entry_point("process")
    graph.add_conditional_edges("process", should_continue)
    graph.add_edge("tools", "process")

    return graph.compile()
```

### 2. LangChain + CopilotKit

```python
from langchain.agents import AgentExecutor
from langchain.chat_models import ChatOpenAI
from copilotkit import copilotkit_emit_state

async def langchain_agent_node(state: MyState):
    """Integrate LangChain agent."""
    llm = ChatOpenAI(model="gpt-4")
    agent = AgentExecutor.from_agent_and_tools(
        agent=agent_type,
        tools=tools,
        llm=llm,
    )

    # Update state before execution
    state["status"] = "running_agent"
    await copilotkit_emit_state(state)

    # Run agent
    result = await agent.arun(state["query"])

    # Update state after execution
    state["result"] = result
    state["status"] = "complete"
    await copilotkit_emit_state(state)

    return state
```

### 3. Anthropic SDK + CopilotKit

```python
from anthropic import AsyncAnthropic
from copilotkit import copilotkit_emit_state

async def claude_streaming_node(state: MyState):
    """Stream responses from Claude."""
    client = AsyncAnthropic()

    state["content"] = ""
    await copilotkit_emit_state(state)

    async with client.messages.stream(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        messages=[{"role": "user", "content": state["prompt"]}],
    ) as stream:
        async for chunk in stream.text_stream:
            state["content"] += chunk
            await copilotkit_emit_state(state)

    return state
```

---

## AG-UI Patterns

### 1. Automatic UI Generation from Pydantic

```python
from pydantic import BaseModel, Field
from copilotkit import CopilotKitState

class UserPreferences(BaseModel):
    """User preferences for research."""
    depth: str = Field(description="Research depth: shallow, medium, deep")
    sources: int = Field(description="Number of sources to cite", ge=1, le=20)
    format: str = Field(description="Output format: markdown, html, pdf")

class AgentState(CopilotKitState):
    preferences: UserPreferences = UserPreferences()

# AG-UI will automatically generate a form for UserPreferences
```

```typescript
// Frontend: AG-UI renders the form automatically
import { AGUIForm } from "@copilotkit/ag-ui";

export function PreferencesForm() {
  return (
    <AGUIForm
      agentName="research_agent"
      stateKey="preferences"
      schema={/* auto-generated from Pydantic */}
      onSubmit={(values) => {
        // Updates agent state automatically
      }}
    />
  );
}
```

---

## Performance Optimization

### 1. Batched State Updates

```python
# ✅ GOOD: Batch updates when appropriate
async def batch_process(state: MyState):
    results = []

    for i, item in enumerate(state["items"]):
        result = await process_item(item)
        results.append(result)

        # Emit every N items, not every single item
        if (i + 1) % 5 == 0:
            state["processed"] = results
            await copilotkit_emit_state(state)

    # Final emit
    state["processed"] = results
    state["status"] = "complete"
    await copilotkit_emit_state(state)

    return state
```

### 2. Lazy Loading Content

```typescript
// Load sections on demand
export function DocumentViewer() {
  const { state } = useCoAgent({ name: "research_agent" });
  const [expandedSections, setExpandedSections] = useState<Set<number>>(new Set());

  return (
    <div>
      {state.sections?.map((section, i) => (
        <div key={i}>
          <button onClick={() => toggleSection(i)}>
            {section.title}
          </button>
          {expandedSections.has(i) && (
            <div>{section.content}</div>
          )}
        </div>
      ))}
    </div>
  );
}
```

---

## Error Handling

### 1. Graceful Error Recovery

```python
from copilotkit import copilotkit_emit_state

async def robust_node(state: MyState):
    try:
        result = await risky_operation()
        state["result"] = result
        state["status"] = "success"
    except Exception as e:
        state["error"] = str(e)
        state["status"] = "error"
        # Emit error state so frontend can show it
        await copilotkit_emit_state(state)

        # Allow user to retry
        feedback = interrupt("error_recovery")
        if feedback.get("retry"):
            return await robust_node(state)  # Retry
        else:
            return state  # Give up

    await copilotkit_emit_state(state)
    return state
```

```typescript
// Frontend: Show error UI
useCoAgentStateRender({
  name: "my_agent",
  render: ({ state }) => {
    if (state.status === "error") {
      return (
        <ErrorAlert
          message={state.error}
          onRetry={() => sendRetrySignal()}
        />
      );
    }
    return null;
  },
});
```

### 2. Timeout Handling

```python
import asyncio

async def with_timeout(state: MyState):
    try:
        result = await asyncio.wait_for(
            long_running_task(),
            timeout=30.0
        )
        state["result"] = result
    except asyncio.TimeoutError:
        state["error"] = "Operation timed out"
        state["status"] = "timeout"

    await copilotkit_emit_state(state)
    return state
```

---

## Best Practices Summary

### Backend (Python)
1. ✅ Always extend `CopilotKitState`
2. ✅ Emit state after significant changes
3. ✅ Use `interrupt()` for user approval
4. ✅ Provide detailed error messages
5. ✅ Use type hints for all state fields
6. ✅ Keep state schemas simple and serializable

### Frontend (TypeScript)
1. ✅ Wrap app with `CopilotKitProvider`
2. ✅ Match state types to Python schema
3. ✅ Use `useCoAgentStateRender` for reactive UI
4. ✅ Handle loading and error states
5. ✅ Provide clear user feedback
6. ✅ Use streaming hooks for long operations

### General
1. ✅ Keep state in sync (Python ↔ TypeScript)
2. ✅ Emit state frequently for better UX
3. ✅ Use interrupts for all user decisions
4. ✅ Test state synchronization thoroughly
5. ✅ Handle errors gracefully on both sides
6. ✅ Optimize for streaming and responsiveness

---

**This patterns guide is a living document. Refer to official CopilotKit docs for the latest updates.**
