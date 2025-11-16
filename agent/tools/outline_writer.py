import json5 as json
from datetime import datetime
from typing import Optional, Dict

from langchain_community.adapters.openai import convert_openai_messages
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

from copilotkit.langchain import copilotkit_emit_state
from langchain_core.runnables import RunnableConfig

# Import Pydantic models for AG-UI support
from state import Proposal, ProposalSection


# "description": "The main sections that compose this research",  # This is a description on what are "sections"
# Define proposal structure keys at module level for single source of truth
PROPOSAL_FORMAT = {
    "sections": {
        "section1": {  # Key is the name of the item
            "title": "Title of the item",
            "description": "Description of section1",
            "approved": False,
            # Defines if this goes in the final structure. Set only important parts to True by default
        }
    },
}

PROPOSAL_KEYS = list(PROPOSAL_FORMAT.keys())

class OutlineWriterInput(BaseModel):
    research_query: str = Field(description="Research query")
    state: Optional[Dict] = Field(description="State of the research")

@tool("outline_writer", args_schema=OutlineWriterInput, return_direct=True)
async def outline_writer(research_query, state):
    """Writes a research outline proposal based on the research query"""
    # Get sources from state
    sources = state.get("sources", {})
    sources_summary = ""
    for url, source in sources.items():
        sources_summary += f"- title: {source['title']}"
        sources_summary += f" url:  {source['url']}"
        sources_summary += f" content:  {source['content']}\n"

    # Check if a current proposal exists
    current_proposal = state.get('proposal', None)
    if current_proposal:
        approved_sections = ""
        non_approved_sections = ""
        # Handle both Pydantic Proposal and dict for backward compatibility
        sections = current_proposal.sections if isinstance(current_proposal, Proposal) else current_proposal.get('sections', {})
        for k, v in sections.items():
            # Handle both ProposalSection objects and dicts
            if isinstance(v, ProposalSection):
                if v.approved:
                    approved_sections += f"\"{v.title}\", "
                else:
                    non_approved_sections += f"\"{v.title}\", "
            elif isinstance(v, dict) and v.get('approved'):
                approved_sections += f"\"{v['title']}\", "
            else:
                non_approved_sections += f"\"{v.get('title', '')}\", "
        # Remove trailing ", "
        approved_sections = approved_sections.rstrip(", ")
        non_approved_sections = non_approved_sections.rstrip(", ")

        # Convert Proposal to dict for JSON serialization
        proposal_data = current_proposal.model_dump() if isinstance(current_proposal, Proposal) else current_proposal
        current_proposal_text = (
            f"Current proposal:\n{json.dumps(proposal_data, indent=2)}\n\n"
            "Consider the user's remarks when drafting the revised proposal and generating new sections. ")
        if approved_sections:
            current_proposal_text += (
                f"Ensure to include the following user approved sections in the new proposal: {approved_sections}. ")
        if non_approved_sections:
            current_proposal_text += (
                f"If the user did not mention in the remarks any edits requests regarding the following non approved sections: {non_approved_sections}, omit those sections from the new proposal."
                )
    else:
        current_proposal_text = ""

    prompt = [{
        "role": "system",
        "content": "You are an AI assistant that helps users plan research structures. "
                   "Your task is to propose a logical structure for a research paper that "
                   "the user can review and modify. "
    }, {
        "role": "user",
        "content": f"Today's date is {datetime.now().strftime('%d/%m/%Y')}\n."
                   f"Research Topic: {research_query}\n"
                   f"Create a detailed proposal that includes report's sections. "
                   f"Please return nothing but a JSON in the "
                   f"following format:\n"
                   f"{json.dumps(PROPOSAL_FORMAT, indent=2)}\n"
                   f"{current_proposal_text}"
                   f"Here are some relevant sources to consider while planning the proposal:\n"
                   f"{sources_summary}\n\n"
                   f"Your Proposal:"
    }]

    config = RunnableConfig()
    state["logs"] = state.get("logs", [])
    state["logs"].append({
        "message": "💭 Thinking of a research proposal",
        "done": False
    })
    await copilotkit_emit_state(config, state)

    state["logs"].append({
        "message": "✨ Generating a research proposal outline",
        "done": False
    })
    state["logs"][-2]["done"] = True
    await copilotkit_emit_state(config, state)

    try:

        lc_messages = convert_openai_messages(prompt)
        optional_params = {
            "response_format": {"type": "json_object"}
        }

        response = ChatOpenAI(model='gpt-4o-mini', max_retries=1, model_kwargs=optional_params).invoke(lc_messages, config).content

        for i, log in enumerate(state["logs"]):
            state["logs"][i]["done"] = True
        await copilotkit_emit_state(config, state)

        proposal_dict = json.loads(response)

        # Validate proposal structure using module-level keys
        if not all(key in proposal_dict for key in PROPOSAL_KEYS):
            raise ValueError(f"Missing required keys in proposal. Required: {PROPOSAL_KEYS}")

        # Convert dict sections to Pydantic ProposalSection objects
        sections = {}
        for key, section_data in proposal_dict.get("sections", {}).items():
            if isinstance(section_data, dict):
                sections[key] = ProposalSection(
                    title=section_data.get("title", ""),
                    description=section_data.get("description", ""),
                    approved=section_data.get("approved", False)
                )

        # Create Pydantic Proposal object for AG-UI
        proposal = Proposal(
            sections=sections,
            approved=False,
            remarks=None  # Reset user remarks if the model included them in the new proposal
        )

        tool_msg = f"Generated the following outline proposal:\n{response}"
        state["proposal"] = proposal

        # Clear logs
        state["logs"] = []
        await copilotkit_emit_state(config, state)

        return state, tool_msg
    except Exception as e:
        # Create fallback Proposal object for AG-UI
        fallback_proposal = Proposal(
            sections={},
            approved=False,
            remarks=f"Error generating proposal: {str(e)}"
        )
        state["proposal"] = fallback_proposal

        # Clear logs
        state["logs"] = []
        await copilotkit_emit_state(config, state)

        return state, f"Error generating outline proposal: {e}"