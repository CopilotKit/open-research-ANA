# BLOG-CANVAS-COPILOTkit - Claude Code Documentation

## Project Overview

**ANA (Agent Native Application)** is an AI-powered research canvas application that helps users create comprehensive, well-sourced research reports through an interactive interface.

### What This App Does

ANA combines:
- **Human-in-the-Loop AI**: Users review and approve AI proposals before execution
- **Real-time Web Research**: Powered by Tavily search and extraction APIs
- **Intelligent Agent Orchestration**: Built with LangGraph for complex workflow management
- **Interactive UI**: CopilotKit provides a seamless chat and canvas experience

### Key Features

1. **Research Workflow**:
   - User asks a research question
   - AI searches the web using Tavily
   - AI proposes an outline/structure
   - User reviews and approves sections
   - AI writes only approved sections
   - Continuous iteration until complete

2. **Interactive Canvas**:
   - Split-view interface (chat + document viewer)
   - Real-time progress indicators
   - Source citations and footnotes
   - Editable document sections

## Architecture

### Two-Component System

#### 1. Frontend (`/frontend`)
- **Framework**: Next.js 15 with App Router
- **React**: v19.0.0-rc
- **UI Library**: shadcn/ui (Radix UI primitives + Tailwind CSS)
- **AI Integration**: CopilotKit (react-core, react-ui, runtime v1.5.20)
- **Package Manager**: pnpm v10.2.1

**Key Components**:
```
src/
├── app/
│   ├── page.tsx              # Main split-view layout
│   ├── layout.tsx            # CopilotKit provider
│   └── api/copilotkit/       # API route
├── components/
│   ├── chat.tsx              # CopilotChat wrapper
│   ├── documents-view.tsx    # Document viewer/editor
│   ├── structure-proposal-viewer.tsx  # Outline approval UI
│   ├── progress.tsx          # Agent progress indicators
│   └── ui/                   # shadcn/ui components
└── lib/
    ├── hooks/                # Custom React hooks
    └── types/                # TypeScript types
```

#### 2. Agent (`/agent`)
- **Framework**: LangGraph (workflow orchestration)
- **Language**: Python 3.12
- **LLM**: OpenAI (via langchain-openai)
- **Search**: Tavily API
- **Integration**: CopilotKit Python SDK v0.1.39

**Agent Architecture**:
```python
ResearchAgent StateGraph:
├── call_model_node      # LLM with tool binding
├── tool_node            # Execute tools (search, extract, write)
└── process_feedback_node # Handle user approval/rejection
```

**Tools**:
- `tavily_search`: Web search
- `tavily_extract`: Content extraction from URLs
- `outline_writer`: Generate research outline
- `section_writer`: Write report sections
- `review_proposal`: Trigger user review (interrupt)

**State Management**:
```python
ResearchState (extends CopilotKitState):
├── title: str
├── proposal: dict           # Proposed outline
├── outline: dict            # Approved outline
├── sections: list[dict]     # Written sections
├── sources: dict            # Citations
├── logs: list[dict]         # Progress logs
└── messages: list           # Conversation history
```

## Tech Stack

### Frontend
- Next.js 15.0.2
- React 19.0.0-rc
- TypeScript
- CopilotKit 1.5.20
- shadcn/ui (NOT AG-UI)
- Radix UI
- Tailwind CSS + animations
- Lucide React (icons)
- React Markdown

### Agent
- Python 3.12
- LangGraph + LangChain
- langchain-openai
- Tavily Python
- CopilotKit SDK
- Pydantic
- python-dotenv

### Infrastructure
- LangGraph CLI (v0.1.71) - agent server
- LangSmith - monitoring/tracing
- Node.js 20 - runtime

## Development Setup

### Prerequisites
- pnpm
- Docker
- LangGraph CLI
- Python 3.12+

### Environment Variables

#### Frontend (`.env` in `/frontend`)
```bash
OPENAI_API_KEY=your_openai_key
LANGSMITH_API_KEY=your_langsmith_key
NEXT_PUBLIC_COPILOT_CLOUD_API_KEY=your_copilot_cloud_key
```

#### Agent (`.env` in `/agent`)
```bash
OPENAI_API_KEY=your_key
TAVILY_API_KEY=your_key
LANGSMITH_API_KEY=your_key
```

### Running Locally

1. **Start the Agent**:
```bash
cd agent
langgraph up
# Note the API URL (e.g., http://localhost:8123)
```

2. **Create Tunnel**:
```bash
npx copilotkit@latest dev --port 8123
```

3. **Start Frontend**:
```bash
cd frontend
pnpm install
pnpm run dev
```

### Running in DevContainer

This project includes a fully configured devcontainer with:
- Claude Code CLI
- Python 3.12
- Node.js 20 + pnpm
- GitHub CLI (gh)
- Vercel CLI
- Docker-in-Docker
- Firewall security (sandboxed environment)

**To use**:
1. Open in VS Code
2. Command: "Reopen in Container"
3. Wait for container build and initialization
4. All tools pre-installed and ready

## Project Structure

```
/
├── .devcontainer/           # Development container config
│   ├── Dockerfile
│   ├── devcontainer.json
│   └── init-firewall.sh
├── .claude/                 # Claude Code configuration
│   ├── commands/            # Custom slash commands
│   └── skills/              # Custom skills
├── agent/                   # Python LangGraph agent
│   ├── graph.py             # Main agent workflow
│   ├── state.py             # State definitions
│   ├── config.py            # LLM config
│   ├── tools/               # Agent tools
│   ├── requirements.txt
│   └── langgraph.json
├── frontend/                # Next.js frontend
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   └── lib/
│   ├── package.json
│   └── tailwind.config.ts
├── CLAUDE.md               # This file
└── README.md               # User-facing README
```

## Design Patterns

### Human-in-the-Loop
The agent uses LangGraph's `interrupt()` feature to pause execution and wait for user approval:
1. Agent generates outline proposal
2. Calls `review_proposal` tool → triggers interrupt
3. Frontend shows `ProposalViewer` component
4. User approves/rejects sections
5. Agent resumes with feedback

### Streaming Content
- Agent emits state updates via `copilotkit_emit_state()`
- Frontend uses `useCoAgentStateRender` to show progress
- `useStreamingContent` hook handles real-time section updates

### State Synchronization
- Agent state (Python) ↔ Frontend state (TypeScript)
- CopilotKit handles bidirectional sync
- `ResearchProvider` context manages frontend state

## UI/UX Design

### Color Palette
- Background: `#FAF9F6` (warm off-white)
- Text: `#3D2B1F` (dark brown)
- Accent: Tailwind defaults with custom theming

### Typography
- UI: Lato (300, 400, 700)
- Content: Noto Serif

### Layout
- Resizable split-view (30-50% chat, rest document)
- Draggable divider with grip handle
- Responsive padding: `px-8 2xl:px-[8vw]`

## Deployment Considerations

### Frontend
- Can deploy to Vercel, Render, or similar
- Requires `NEXT_PUBLIC_COPILOT_CLOUD_API_KEY` or local runtime

### Agent
- Deploy via LangGraph Cloud
- Or self-host using `langgraph up` + tunnel

### Security
- Devcontainer includes firewall for sandboxed development
- Whitelist: GitHub, NPM, PyPI, OpenAI, Tavily, LangSmith, CopilotKit

## Known Limitations

- ❌ Not containerized for production (only devcontainer)
- ❌ No AG-UI integration (uses shadcn/ui instead)
- ❌ No Dockerfile for standalone deployment
- ⚠️ Requires external APIs (OpenAI, Tavily, LangSmith)

## Future Enhancements

- [ ] Add AG-UI integration for Pydantic agents
- [ ] Containerize for production deployment
- [ ] Add offline/local LLM support
- [ ] Implement caching for Tavily searches
- [ ] Add export formats (PDF, DOCX, Markdown)
- [ ] Multi-user collaboration features

## Contributing

When working on this project:
1. Frontend changes: Work in `/frontend`, use `pnpm`
2. Agent changes: Work in `/agent`, test with `langgraph up`
3. Always test full workflow (search → outline → approval → write)
4. Update this CLAUDE.md when adding features

## Useful Commands

### Frontend
```bash
pnpm dev              # Start dev server
pnpm build            # Build for production
pnpm lint             # Run ESLint
```

### Agent
```bash
langgraph up          # Start agent server
langgraph dev         # Start with hot reload
pip install -r requirements.txt  # Install dependencies
```

### DevContainer
```bash
sudo /usr/local/bin/init-firewall.sh  # Reinitialize firewall
claude                 # Launch Claude Code CLI
gh auth login          # Authenticate GitHub CLI
```

## Resources

- [CopilotKit Docs](https://docs.copilotkit.ai/coagents)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [Tavily API](https://tavily.com/)
- [shadcn/ui](https://ui.shadcn.com/)

---

*Last Updated: 2025-11-08*
*Maintained for Claude Code development*
