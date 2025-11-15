# CopilotKit Expert Plugin for Claude Code

A comprehensive, reusable plugin that transforms Claude Code into a CopilotKit expert with deep knowledge of CoAgents, AG-UI, and AI framework integrations.

## 🎯 What This Plugin Provides

### Expert AI Agent
A specialized **CopilotKit Expert Agent** with expertise in:
- CopilotKit framework (v1.5.20+)
- AG-UI integration
- LangGraph orchestration
- LangChain patterns
- Anthropic Claude SDK
- OpenAI integration
- Human-in-the-loop workflows
- State management and streaming

### MCP Integration
Direct access to **CopilotKit VIBE CODING MCP** for:
- Real-time official documentation
- Code examples from CopilotKit repos
- Best practices and patterns
- Version-specific guidance

### Slash Commands
Quick-access commands for common tasks:
- `/copilotkit-docs` - Search and fetch CopilotKit documentation
- `/copilotkit-integrate` - Guide for integrating CopilotKit features
- `/copilotkit-debug` - Debug CopilotKit issues (state sync, streaming, interrupts)

### Knowledge Base
Comprehensive patterns and best practices guide:
- Core patterns (CoAgent setup, state management)
- Streaming patterns (content generation, progress indicators)
- Human-in-the-loop workflows (approval patterns, interrupts)
- Framework integrations (LangGraph, LangChain, Anthropic)
- AG-UI patterns (auto-form generation)
- Performance optimization
- Error handling

## 📦 Installation

### In This Repository

The plugin is already installed! It's in `.claude/` with:

```
.claude/
├── skills/
│   └── copilotkit-expert.md          # Main expert agent
├── commands/
│   ├── copilotkit-docs.md            # Documentation search
│   ├── copilotkit-integrate.md       # Integration guide
│   └── copilotkit-debug.md           # Debugging helper
├── copilotkit-patterns.md            # Patterns & best practices
└── COPILOTKIT_PLUGIN.md              # This file
```

### In Other Repositories (Reusable)

To use this plugin in other projects:

#### Option 1: Copy Files

```bash
# From this repo, copy the plugin files
cp -r .claude/skills/copilotkit-expert.md /path/to/other/repo/.claude/skills/
cp -r .claude/commands/copilotkit-*.md /path/to/other/repo/.claude/commands/
cp .claude/copilotkit-patterns.md /path/to/other/repo/.claude/
```

#### Option 2: Git Submodule

```bash
cd /path/to/other/repo
git submodule add <this-repo-url> .claude/modules/copilotkit-plugin
ln -s .claude/modules/copilotkit-plugin/skills/copilotkit-expert.md .claude/skills/
ln -s .claude/modules/copilotkit-plugin/commands/copilotkit-*.md .claude/commands/
```

#### Option 3: npm Package (Future)

```bash
npx create-claude-plugin copilotkit-expert
```

### MCP Server Setup

Configure the CopilotKit VIBE CODING MCP:

```bash
claude mcp add --transport sse copilotkit-mcp https://mcp.copilotkit.ai/sse
```

Verify it's active:

```bash
claude mcp list
# Should show: copilotkit-mcp (https://mcp.copilotkit.ai/sse)
```

## 🚀 Usage

### Activating the Expert Agent

The CopilotKit Expert is available as a **skill** in Claude Code. Activate it when you need CopilotKit expertise:

```
User: I need help implementing a human-in-the-loop workflow with CopilotKit

Claude: I'll activate the CopilotKit Expert skill to help you with this.
        [Loads copilotkit-expert skill]

        [Provides expert guidance on interrupts, state management, etc.]
```

Or explicitly request it:

```
User: Use the copilotkit-expert skill to help me debug state synchronization
```

### Using Slash Commands

#### Search Documentation

```
/copilotkit-docs

# Then specify what you want to search:
> How do I use useCoAgentStateRender?
```

#### Integrate a Feature

```
/copilotkit-integrate

# Then describe the feature:
> I want to add a progress indicator that shows real-time agent status
```

#### Debug Issues

```
/copilotkit-debug

# Then describe the problem:
> My frontend isn't receiving state updates from the agent
```

### Accessing Patterns Guide

The patterns guide is available at `.claude/copilotkit-patterns.md`. Reference it for:
- Complete code examples
- Best practices
- Common patterns
- Framework integration examples

## 🧠 How the Expert Agent Works

### Knowledge Sources

1. **Built-in Expertise**: Pre-trained knowledge of CopilotKit patterns
2. **MCP Access**: Real-time docs from https://mcp.copilotkit.ai/sse
3. **Patterns Guide**: Local knowledge base at `.claude/copilotkit-patterns.md`
4. **Project Context**: Understands your current project structure

### Capabilities

#### Code Generation
```typescript
// The agent can generate complete, working code like:
import { useCoAgent, useCoAgentStateRender } from "@copilotkit/react-core";

export function MyCoAgent() {
  const { state, setState } = useCoAgent({
    name: "my_agent",
    initialState: { /* ... */ }
  });

  useCoAgentStateRender({
    name: "my_agent",
    render: ({ state }) => {
      // Custom rendering logic
    }
  });

  return /* UI */;
}
```

#### Architecture Guidance
- Recommends appropriate frameworks for your use case
- Explains trade-offs between different approaches
- Provides state management strategies
- Suggests performance optimizations

#### Debugging
- Diagnoses state synchronization issues
- Identifies streaming problems
- Fixes interrupt/approval workflows
- Resolves type mismatches

#### Best Practices
- Enforces CopilotKit patterns
- Ensures type safety
- Optimizes for performance
- Handles errors gracefully

## 📚 Examples

### Example 1: Creating a CoAgent

```
User: Help me create a CoAgent that generates research reports

CopilotKit Expert:
I'll help you create a research report CoAgent. Here's the complete implementation:

[Backend - state.py]
... (provides complete Python code)

[Backend - graph.py]
... (provides LangGraph setup)

[Frontend - components/ResearchAgent.tsx]
... (provides React component)

This pattern uses:
- State synchronization via copilotkit_emit_state()
- Streaming content updates
- Human-in-the-loop approval workflow
- Progress indicators

Try it by:
1. Start agent: cd agent && langgraph up
2. Start frontend: cd frontend && pnpm dev
3. Test the workflow end-to-end
```

### Example 2: Debugging State Sync

```
User: My state updates aren't showing in the frontend

CopilotKit Expert:
Let me help debug this state synchronization issue.

First, let's verify:
1. Is copilotkit_emit_state() called after state changes?
   [Checks agent code]

2. Does the state schema match TypeScript types?
   [Compares state.py vs types.ts]

3. Is the CopilotKit provider configured correctly?
   [Checks layout.tsx]

I found the issue: [explains specific problem]

Here's the fix: [provides corrected code]

After applying this fix, you should see state updates in real-time.
```

### Example 3: Adding AG-UI

```
User: How do I add AG-UI to generate forms from my Pydantic models?

CopilotKit Expert:
AG-UI can automatically generate forms from Pydantic models. Here's how:

[Step 1: Define Pydantic Model]
... (shows Python code)

[Step 2: Install AG-UI]
... (shows npm command)

[Step 3: Create Form Component]
... (shows React component with AG-UI)

[Step 4: Integrate with CoAgent]
... (shows integration code)

This will generate a fully functional form with:
- Automatic field types
- Validation from Pydantic
- Submit handling
- Error display
```

## 🎨 Customization

### Extending the Expert

Add your own patterns to `.claude/copilotkit-patterns.md`:

```markdown
## My Custom Pattern

### Use Case
Describe when to use this pattern

### Implementation
```code examples```

### Best Practices
- Tip 1
- Tip 2
```

### Adding Commands

Create new slash commands in `.claude/commands/`:

```markdown
---
description: My custom CopilotKit command
---

Command instructions here...
```

### Configuring MCP

Add additional MCP servers for extended capabilities:

```bash
claude mcp add --transport stdio my-custom-mcp /path/to/server
```

## 🔧 Troubleshooting

### MCP Not Connected

```bash
# Check MCP status
claude mcp list

# Reconnect if needed
claude mcp remove copilotkit-mcp
claude mcp add --transport sse copilotkit-mcp https://mcp.copilotkit.ai/sse
```

### Skill Not Loading

Verify file locations:
```bash
ls -la .claude/skills/copilotkit-expert.md
ls -la .claude/commands/copilotkit-*.md
```

### Commands Not Appearing

Ensure frontmatter is correct:
```markdown
---
description: Brief description here
---
```

## 🌐 Using Across Projects

### Cloud Repositories

Works seamlessly in cloud environments (GitHub Codespaces, etc.):
1. Clone your repo with the plugin
2. Claude Code automatically detects `.claude/` config
3. MCP connection works via SSE (no local setup needed)

### Local Development

Same setup process:
1. Install Claude Code CLI
2. Copy plugin files to `.claude/`
3. Configure MCP server
4. Start using immediately

### Team Sharing

Share the plugin with your team:
1. Commit `.claude/` directory to git
2. Team members get the plugin automatically
3. Everyone has the same CopilotKit expertise

## 📖 Resources

### Official Documentation
- [CopilotKit Docs](https://docs.copilotkit.ai/)
- [CoAgents Guide](https://docs.copilotkit.ai/coagents)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [Claude Code Docs](https://docs.claude.com/en/docs/claude-code)

### Plugin Files
- **Expert Agent**: `.claude/skills/copilotkit-expert.md`
- **Patterns Guide**: `.claude/copilotkit-patterns.md`
- **Commands**: `.claude/commands/copilotkit-*.md`

### Support
- [CopilotKit Discord](https://discord.gg/copilotkit)
- [GitHub Issues](https://github.com/CopilotKit/CopilotKit/issues)
- [Claude Code GitHub](https://github.com/anthropics/claude-code)

## 🚢 Version

- **Plugin Version**: 1.0.0
- **CopilotKit Compatibility**: v1.5.20+
- **Claude Code**: Latest
- **Last Updated**: 2025-11-15

## 📝 License

This plugin is part of the BLOG-CANVAS-COPILOTkit project. Reusable across projects.

---

**Ready to become a CopilotKit expert? Activate the skill or use a slash command to get started!**
