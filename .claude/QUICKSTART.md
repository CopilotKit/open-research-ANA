# CopilotKit Plugin - Quick Start Guide

Get started with the CopilotKit Expert Plugin in under 5 minutes!

## 🎯 What You'll Learn

- How to use the CopilotKit Expert skill
- How to use CopilotKit slash commands
- Common workflows and examples
- How to leverage the MCP integration

## ⚡ Quick Examples

### Example 1: Getting Help with CopilotKit

**Scenario**: You want to understand how `useCoAgentStateRender` works.

```
You: How do I use useCoAgentStateRender to show real-time agent state?

Claude (activates copilotkit-expert skill):
useCoAgentStateRender is a hook that lets you render UI based on agent state changes.

Here's a complete example:

[Provides detailed TypeScript code with explanations]

The key points are:
1. It subscribes to state updates from your CoAgent
2. You provide a render function that returns JSX
3. The component re-renders automatically when state changes
4. Great for progress indicators, approval UIs, etc.

In this project, you can see it used in:
- frontend/src/components/structure-proposal-viewer.tsx
- frontend/src/components/progress.tsx
```

**Alternative using slash command**:
```
You: /copilotkit-docs

Claude: What CopilotKit documentation would you like to explore?

You: useCoAgentStateRender hook

Claude (uses MCP to fetch official docs):
[Fetches and displays official documentation with examples]
```

### Example 2: Implementing a New Feature

**Scenario**: Add a progress indicator to your CoAgent.

```
You: I want to add a progress indicator that shows which step my agent is on

Claude (activates copilotkit-expert skill):
I'll help you add a progress indicator with real-time updates.

Backend (agent/state.py):
---
[Provides Python code to add progress tracking to state]

Backend (agent/graph.py):
---
[Shows how to emit progress updates]

Frontend (components/ProgressIndicator.tsx):
---
[Complete React component with useCoAgentStateRender]

Implementation Steps:
1. Update state schema with progress field
2. Emit state after each step in the agent
3. Create progress component in frontend
4. Add component to your layout

Test it by:
1. Start agent and frontend
2. Trigger a workflow
3. Watch the progress indicator update in real-time
```

**Alternative using slash command**:
```
You: /copilotkit-integrate

Claude: What CopilotKit feature would you like to integrate?

You: A progress indicator showing agent steps

Claude:
[Provides detailed integration guide with checklist]
[Shows exactly what files to modify]
[Includes testing steps]
```

### Example 3: Debugging State Synchronization

**Scenario**: Your frontend isn't receiving agent state updates.

```
You: My frontend isn't showing agent state updates. The state seems stuck.

Claude (activates copilotkit-expert skill):
Let me help debug this state synchronization issue.

I'll check the common causes:

1. State Emission (Backend)
   ✅ Checking if copilotkit_emit_state() is called...
   [Analyzes agent code]

2. State Schema Matching
   ✅ Comparing Python state vs TypeScript types...
   [Compares state.py and types.ts]

3. Provider Configuration
   ✅ Checking CopilotKitProvider setup...
   [Reviews layout.tsx]

Found the issue:
In agent/graph.py:156, you're updating state but not emitting it.

Fix:
[Shows exact code change needed]

After this fix, your frontend will receive state updates immediately.
```

**Alternative using slash command**:
```
You: /copilotkit-debug

Claude: What CopilotKit issue are you experiencing?

You: State not syncing to frontend

Claude:
[Runs diagnostic workflow]
[Identifies specific problem]
[Provides fix with explanation]
[Shows verification steps]
```

### Example 4: Learning About AG-UI

**Scenario**: You want to auto-generate forms from Pydantic models.

```
You: How do I use AG-UI to generate forms from my Pydantic agent models?

Claude (activates copilotkit-expert skill):
AG-UI automatically generates beautiful forms from Pydantic models. Here's how:

Step 1: Define Your Pydantic Model
---
[Shows Python Pydantic model with Field descriptions]

Step 2: Install AG-UI
---
[Shows npm install command]

Step 3: Create the Form Component
---
[Complete React component using AG-UI]

Step 4: Integrate with CoAgent
---
[Shows how to connect form to agent state]

The result:
- Automatic field types from Pydantic
- Built-in validation
- Professional styling
- Submit handling
- Error display

You can customize:
- Field layouts
- Validation messages
- Styling/theming
- Submit behavior
```

### Example 5: Multi-Framework Integration

**Scenario**: Use LangGraph + Anthropic SDK + CopilotKit together.

```
You: How do I integrate Claude's streaming with my LangGraph CoAgent?

Claude (activates copilotkit-expert skill):
Great question! You can combine LangGraph orchestration with Claude's
streaming capabilities. Here's the pattern:

Architecture:
1. LangGraph manages the workflow
2. Anthropic SDK handles Claude streaming
3. CopilotKit synchronizes state to frontend

Implementation:
---
[Shows complete Python code integrating all three]

Key Points:
1. Create async streaming node in LangGraph
2. Use Anthropic's async streaming client
3. Emit state on each chunk for real-time updates
4. Handle errors gracefully

Frontend:
---
[Shows React component to display streaming content]

This pattern gives you:
✅ Structured workflow (LangGraph)
✅ Streaming responses (Anthropic)
✅ Real-time UI updates (CopilotKit)
```

## 🛠️ Common Workflows

### Workflow 1: Starting a New CoAgent

1. **Ask for architecture guidance**:
   ```
   "I want to create a CoAgent that [describe functionality]"
   ```

2. **Get complete implementation**:
   - Backend state schema (Python)
   - LangGraph workflow
   - Frontend hooks and components
   - Testing instructions

3. **Implement step-by-step**:
   - Follow provided code examples
   - Test as you go
   - Iterate with feedback

### Workflow 2: Adding a Feature

1. **Use the integration command**:
   ```
   /copilotkit-integrate
   ```

2. **Describe the feature**:
   ```
   "Add user approval workflow for generated sections"
   ```

3. **Follow the checklist**:
   - Backend changes
   - Frontend changes
   - Integration testing

### Workflow 3: Debugging Issues

1. **Use the debug command**:
   ```
   /copilotkit-debug
   ```

2. **Describe the problem**:
   ```
   "Interrupts aren't triggering in my agent"
   ```

3. **Apply suggested fixes**:
   - Review diagnostics
   - Implement fixes
   - Verify solution

### Workflow 4: Learning Patterns

1. **Search documentation**:
   ```
   /copilotkit-docs
   ```

2. **Or ask directly**:
   ```
   "Show me best practices for state management in CopilotKit"
   ```

3. **Reference patterns guide**:
   - Check `.claude/copilotkit-patterns.md`
   - Find relevant pattern
   - Adapt to your use case

## 📖 Understanding the Plugin Components

### The Expert Agent (Skill)
- **File**: `.claude/skills/copilotkit-expert.md`
- **When it activates**: Automatically when you ask CopilotKit questions
- **What it knows**: CopilotKit, AG-UI, LangGraph, LangChain, Anthropic, OpenAI
- **What it does**: Provides code, explains patterns, debugs issues

### Slash Commands
- **`/copilotkit-docs`**: Fetch official documentation via MCP
- **`/copilotkit-integrate`**: Step-by-step integration guide
- **`/copilotkit-debug`**: Diagnostic and debugging workflow

### Patterns Guide
- **File**: `.claude/copilotkit-patterns.md`
- **Contains**: Complete code examples, best practices, anti-patterns
- **Use when**: You need reference implementations

### MCP Integration
- **Server**: CopilotKit VIBE CODING MCP
- **URL**: https://mcp.copilotkit.ai/sse
- **Provides**: Real-time official docs, code examples, API references

## 🎓 Learning Path

### Beginner
1. Use `/copilotkit-docs` to explore basic concepts
2. Ask "How do I create a basic CoAgent?"
3. Review patterns guide for simple examples
4. Build your first CoAgent with guidance

### Intermediate
1. Ask about state management patterns
2. Learn human-in-the-loop workflows
3. Implement streaming content
4. Use `/copilotkit-integrate` for new features

### Advanced
1. Explore multi-framework integrations
2. Learn AG-UI auto-generation
3. Optimize performance
4. Build complex multi-agent systems

## 💡 Pro Tips

### Tip 1: Be Specific
```
❌ "How does CopilotKit work?"
✅ "How do I emit state from my LangGraph agent to update the frontend?"
```

### Tip 2: Use the Right Tool
- **Quick docs lookup** → `/copilotkit-docs`
- **Feature implementation** → `/copilotkit-integrate`
- **Debugging** → `/copilotkit-debug`
- **Complex questions** → Just ask (expert agent activates)

### Tip 3: Reference Existing Code
```
"How can I modify frontend/src/components/documents-view.tsx to add
a new streaming section viewer?"
```

The expert understands your project structure and can give targeted advice.

### Tip 4: Ask for Comparisons
```
"What's the difference between useCoAgent and useCoAgentStateRender?"
"When should I use interrupt() vs regular state emission?"
```

### Tip 5: Request Complete Examples
```
"Show me a complete example of a CoAgent with:
- State synchronization
- Streaming content
- User approval workflow
- Error handling"
```

## 🚀 Your First 5 Minutes

Try this right now:

```
You: /copilotkit-docs

Claude: What CopilotKit documentation would you like to explore?

You: CoAgent basics

Claude: [Fetches and explains CoAgent concepts with examples]
```

Then:

```
You: Show me how the research agent in this project uses CoAgents

Claude: [Analyzes agent/graph.py and explains the implementation]
```

Finally:

```
You: /copilotkit-integrate

Claude: What CopilotKit feature would you like to integrate?

You: I want to add a "save draft" feature that stores partial research

Claude: [Provides complete implementation plan]
```

## 📚 Next Steps

1. **Explore the patterns guide**: Open `.claude/copilotkit-patterns.md`
2. **Read plugin docs**: Check `.claude/COPILOTKIT_PLUGIN.md`
3. **Try examples**: Implement one of the examples above
4. **Ask questions**: The expert is always available!

## ❓ FAQ

**Q: When should I use a slash command vs asking directly?**

A: Use slash commands for structured workflows (integration, debugging).
   Ask directly for explanations, examples, and general questions.

**Q: Can the expert help with other frameworks besides CopilotKit?**

A: Yes! It knows LangGraph, LangChain, Anthropic SDK, OpenAI, and can
   help integrate them with CopilotKit.

**Q: Does the MCP need to be connected?**

A: The expert works without MCP, but MCP provides access to the latest
   official documentation and examples.

**Q: Can I use this plugin in other projects?**

A: Absolutely! Copy `.claude/skills/copilotkit-expert.md`, the commands,
   and patterns guide to any project.

**Q: How do I know if the expert agent is activated?**

A: Claude will use its knowledge of CopilotKit to answer your questions.
   The quality and depth of CopilotKit-specific answers indicate activation.

## 🎉 Ready to Go!

You now know how to:
- ✅ Use the CopilotKit Expert skill
- ✅ Run slash commands
- ✅ Debug issues
- ✅ Integrate features
- ✅ Learn patterns

**Start building amazing CoAgents!** 🚀

---

*Need more help? Just ask! The CopilotKit Expert is here to help you succeed.*
