# Claude Code Configuration

This directory contains Claude Code customizations for the BLOG-CANVAS-COPILOTkit project.

## Structure

```
.claude/
├── commands/           # Custom slash commands
│   ├── start-dev.md           # Start full dev environment
│   ├── check-health.md        # Health check all services
│   ├── add-feature.md         # Feature addition guide
│   ├── debug-agent.md         # Agent debugging workflow
│   ├── update-deps.md         # Dependency update guide
│   ├── copilotkit-docs.md     # CopilotKit documentation search
│   ├── copilotkit-integrate.md # CopilotKit integration guide
│   └── copilotkit-debug.md    # CopilotKit debugging helper
├── skills/             # Custom skills
│   └── copilotkit-expert.md   # CopilotKit Expert Agent
├── copilotkit-patterns.md # CopilotKit patterns & best practices
├── COPILOTKIT_PLUGIN.md   # CopilotKit plugin documentation
└── README.md          # This file
```

## Available Slash Commands

### `/start-dev`
Starts the complete development environment:
- LangGraph agent server
- CopilotKit tunnel
- Frontend dev server

**Usage**: `/start-dev`

### `/check-health`
Performs comprehensive health check:
- Service status (agent, frontend)
- Environment configuration
- Dependencies
- API connectivity
- Port availability

**Usage**: `/check-health`

### `/add-feature`
Interactive guide for adding new features:
- Analyzes feature requirements
- Provides implementation plan
- Guides through frontend/agent/full-stack changes
- Includes testing checklist

**Usage**: `/add-feature` then describe your feature

### `/debug-agent`
Debug LangGraph agent issues:
- Analyzes agent logs
- Checks configuration
- Tests state and tools
- Reviews system prompts
- Suggests fixes for common issues

**Usage**: `/debug-agent`

### `/update-deps`
Safely update project dependencies:
- Checks current versions
- Shows available updates
- Provides update strategy
- Runs update process
- Verifies functionality

**Usage**: `/update-deps`

### `/copilotkit-docs`
Search and fetch CopilotKit documentation using VIBE CODING MCP:
- Search official docs
- Get code examples
- Access latest API references
- Version-specific guidance

**Usage**: `/copilotkit-docs` then specify what to search for

### `/copilotkit-integrate`
Guide for integrating CopilotKit features:
- Plans frontend/backend integration
- Provides implementation checklist
- Shows code examples
- Tests integration

**Usage**: `/copilotkit-integrate` then describe the feature

### `/copilotkit-debug`
Debug CopilotKit integration issues:
- State synchronization problems
- Streaming content issues
- Interrupt/approval workflows
- Type mismatches
- Performance issues

**Usage**: `/copilotkit-debug` then describe the issue

## Available Skills

### `copilotkit-expert`
Specialized AI agent expert in CopilotKit framework:
- Deep knowledge of CoAgents, AG-UI, and integrations
- Supports LangGraph, LangChain, Anthropic SDK, OpenAI
- Provides complete working examples
- Debugging and optimization guidance
- Access to VIBE CODING MCP for real-time docs

**Activation**: The skill activates automatically when CopilotKit topics are discussed, or request it explicitly.

**See**: [COPILOTKIT_PLUGIN.md](./COPILOTKIT_PLUGIN.md) for full documentation

## 🚀 CopilotKit Plugin

This project includes a comprehensive **CopilotKit Expert Plugin** that provides:
- **Expert Agent**: Specialized in CopilotKit, AG-UI, and AI frameworks
- **MCP Integration**: Real-time access to official CopilotKit docs
- **Slash Commands**: Quick access to docs, integration, and debugging
- **Patterns Guide**: Complete reference of best practices

### Quick Start with CopilotKit Plugin

1. **Use Slash Commands**:
   ```
   /copilotkit-docs
   /copilotkit-integrate
   /copilotkit-debug
   ```

2. **Activate Expert Agent**: Just ask CopilotKit questions
   ```
   "How do I implement human-in-the-loop with CopilotKit?"
   ```

3. **Reference Patterns**: Check `copilotkit-patterns.md` for examples

**Full Plugin Documentation**: [COPILOTKIT_PLUGIN.md](./COPILOTKIT_PLUGIN.md)

## Creating Custom Commands

To create a new slash command:

1. Create a new `.md` file in `.claude/commands/`
2. Add frontmatter with description:
   ```markdown
   ---
   description: Brief description of what this command does
   ---

   Command prompt content here...
   ```
3. The command name will be the filename (e.g., `my-command.md` → `/my-command`)

## Creating Custom Skills

Skills are reusable, specialized agents that can be invoked during conversations.

To create a skill:

1. Create a new `.md` file in `.claude/skills/`
2. Add frontmatter with description
3. Define the skill's capabilities and workflow

Skills are invoked differently than commands - they run as specialized sub-agents.

## Project Context

Claude Code has access to:
- Full codebase (frontend + agent)
- `CLAUDE.md` - comprehensive project documentation
- Git history and status
- Environment files (.env.example)

For best results:
- Use specific commands for specific tasks
- Refer to CLAUDE.md for architecture details
- Check health before debugging
- Use start-dev for quick setup

## Tips for Working with Claude Code

1. **Use slash commands proactively**: Commands like `/check-health` can prevent issues
2. **Leverage context**: Claude understands the full project structure
3. **Iterate incrementally**: Use `/add-feature` to plan before implementing
4. **Debug systematically**: `/debug-agent` follows a logical debugging flow
5. **Keep deps updated**: Regular `/update-deps` prevents drift

## Resources

### Project Documentation
- [Project README](../README.md)
- [Project Documentation (CLAUDE.md)](../CLAUDE.md)
- [CopilotKit Plugin Documentation](./COPILOTKIT_PLUGIN.md)
- [CopilotKit Patterns & Best Practices](./copilotkit-patterns.md)

### Official Documentation
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
- [CopilotKit Docs](https://docs.copilotkit.ai/)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [Anthropic Claude Docs](https://docs.anthropic.com/)
