# AG-UI Migration Guide

**Date**: 2025-11-15
**CopilotKit Expert Plugin**: v1.0.0
**Migration Status**: ✅ Completed

## Overview

This document describes the migration from custom CopilotKit implementation to AG-UI (Automatic UI Generation) framework. AG-UI automatically generates forms from Pydantic models, eliminating the need for manual form creation and improving type safety across the stack.

## What is AG-UI?

AG-UI is part of the CopilotKit framework that:
- Automatically generates forms from Pydantic models with `Field(description=...)` annotations
- Provides bidirectional type safety between Python backend and TypeScript frontend
- Simplifies human-in-the-loop workflows by handling form rendering automatically
- Works seamlessly with LangGraph's `interrupt()` pattern

## Migration Summary

### Changes Made

#### 1. Backend (Python)

**File: `agent/state.py`**
- ✅ Created Pydantic BaseModel classes for all nested structures:
  - `ProposalSection`: Section in research proposal
  - `Proposal`: Complete proposal structure
  - `Section`: Written section of report
  - `Source`: Research source
  - `Log`: Progress log entry
- ✅ Updated `ResearchState` to use Pydantic models with Field descriptions
- ✅ All fields now have proper type hints and descriptions for AG-UI

**File: `agent/graph.py`**
- ✅ Updated `process_feedback_node` to work with Pydantic `Proposal` objects
- ✅ Added import for new Pydantic models
- ✅ Updated feedback processing logic for Pydantic attributes

**File: `agent/tools/outline_writer.py`**
- ✅ Converts JSON response to Pydantic `Proposal` objects
- ✅ Creates `ProposalSection` objects for each section
- ✅ Backward compatibility with dict format

**File: `agent/tools/section_writer.py`**
- ✅ Creates Pydantic `Section` objects instead of dicts
- ✅ Handles both `Section` objects and dicts for backward compatibility
- ✅ Updated state section management to use Pydantic models

#### 2. Frontend (TypeScript)

**File: `frontend/src/app/api/copilotkit/route.ts`**
- ✅ Migrated from `langGraphPlatformEndpoint` to `LangGraphAgent`
- ✅ New configuration syntax: `agents: {}` instead of `remoteEndpoints: []`
- ✅ Added `graphId: 'agent'` matching `langgraph.json`

**File: `frontend/src/lib/types.ts`**
- ✅ Updated all interfaces to match Pydantic models exactly:
  - `Section`: Now matches backend `Section` model
  - `Proposal`: Direct mapping to backend `Proposal` model
  - `ProposalSection`: Matches backend `ProposalSection` model
  - `Log`: Changed `done: boolean` to `status: string`
  - `Source`: Updated to match backend `Source` model
- ✅ Added comments indicating AG-UI compatibility
- ✅ Maintained backward compatibility where possible

**File: `frontend/src/components/structure-proposal-viewer.tsx`**
- ✅ Updated to use new `Proposal` structure (`proposal.sections` instead of `proposal[ProposalSectionName.Sections]`)
- ✅ Simplified component logic to work with direct field access
- ✅ Updated state management for new Pydantic-based types
- ✅ Maintained existing UI/UX

## Before and After

### Before (Custom Implementation)

#### Backend State
```python
class ResearchState(CopilotKitState):
    title: str
    proposal: Dict[str, Union[str, bool, Dict[str, Union[str, bool]]]]
    sections: List[dict]
    logs: List[dict]
```

#### Frontend Runtime
```typescript
const runtime = new CopilotRuntime({
    remoteEndpoints: [
        langGraphPlatformEndpoint({
            deploymentUrl: deploymentUrl!,
            agents: [{name: 'agent', description: '...'}],
        })
    ]
});
```

### After (AG-UI)

#### Backend State
```python
class ProposalSection(BaseModel):
    title: str = Field(description="The title of the section")
    description: str = Field(description="A brief description...")
    approved: bool = Field(default=False, description="Whether approved...")

class Proposal(BaseModel):
    sections: Dict[str, ProposalSection] = Field(...)
    remarks: Optional[str] = Field(...)
    approved: bool = Field(...)

class ResearchState(CopilotKitState):
    proposal: Optional[Proposal] = Field(...)
    sections: List[Section] = Field(...)
    logs: List[Log] = Field(...)
```

#### Frontend Runtime
```typescript
const runtime = new CopilotRuntime({
    agents: {
        'agent': new LangGraphAgent({
            deploymentUrl: deploymentUrl!,
            graphId: 'agent',
            langsmithApiKey: process.env.LANGSMITH_API_KEY,
        }),
    }
});
```

## Key Benefits

### 1. Type Safety
- ✅ **Backend**: Pydantic validates all data structures
- ✅ **Frontend**: TypeScript interfaces match Pydantic models exactly
- ✅ **Runtime**: Type errors caught at development time

### 2. Automatic Form Generation
- ✅ AG-UI can generate forms from Pydantic models automatically
- ✅ Field descriptions become form labels/hints
- ✅ Validation rules from Pydantic enforced in UI

### 3. Maintainability
- ✅ Single source of truth for state structure (Pydantic models)
- ✅ Easier to add new fields (just update Pydantic model)
- ✅ Less boilerplate code

### 4. CopilotKit Integration
- ✅ Follows official CopilotKit best practices
- ✅ Better integration with `interrupt()` pattern
- ✅ Cleaner state emission with `copilotkit_emit_state()`

## Migration Checklist

- [x] Convert backend state to Pydantic BaseModel with Field descriptions
- [x] Update graph nodes to use Pydantic objects
- [x] Update tools to create Pydantic objects
- [x] Migrate CopilotRuntime to LangGraphAgent syntax
- [x] Update frontend types to match Pydantic models
- [x] Update frontend components to use new structure
- [x] Test state synchronization
- [x] Document migration process

## Testing

### 1. Backend Tests

```bash
cd agent
# Ensure Pydantic models validate correctly
python -c "from state import Proposal, ProposalSection; print(Proposal(sections={}, approved=False, remarks=None))"
# Should output: sections={} approved=False remarks=None
```

### 2. Frontend Build

```bash
cd frontend
pnpm build
# Should complete without TypeScript errors
```

### 3. End-to-End Flow

1. Start agent: `cd agent && langgraph up`
2. Start frontend: `cd frontend && pnpm dev`
3. Create research query
4. Verify proposal generation
5. Test approval workflow
6. Verify section writing

## Troubleshooting

### Issue: Type mismatches between frontend and backend

**Solution**: Ensure TypeScript types match Pydantic models exactly. Check:
- Field names (case-sensitive)
- Optional vs required fields
- Default values

### Issue: State not syncing

**Solution**: Verify:
- `copilotkit_emit_state()` is called after state updates
- Pydantic models serialize correctly (`model.model_dump()`)
- Frontend types are compatible

### Issue: AG-UI form not rendering

**Solution**: Ensure:
- All Pydantic fields have `Field(description=...)`
- `interrupt()` is called with correct state
- `LangGraphAgent` configuration is correct

## Future Enhancements

- [ ] Add AG-UI auto-generated forms alongside custom ProposalViewer
- [ ] Implement form validation from Pydantic validators
- [ ] Add more comprehensive Field descriptions for better UX
- [ ] Create reusable Pydantic models library
- [ ] Add unit tests for Pydantic models

## References

- [CopilotKit AG-UI Documentation](https://docs.copilotkit.ai/langgraph/troubleshooting/migrate-to-agui)
- [CopilotKit Pydantic Guide](https://docs.copilotkit.ai/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)

## Credits

**Migration performed by**: CopilotKit Expert Plugin v1.0.0
**Pattern source**: `.claude/copilotkit-patterns.md`
**Plugin documentation**: `.claude/COPILOTKIT_PLUGIN.md`

---

*This migration follows official CopilotKit best practices and AG-UI migration guidelines.*
