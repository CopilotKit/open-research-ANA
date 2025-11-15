from datetime import datetime
from typing import Optional, Dict, cast
from langchain_core.messages import AIMessage, ToolMessage
from langchain_community.adapters.openai import convert_openai_messages
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
import random
import string
from copilotkit.langchain import copilotkit_customize_config, copilotkit_emit_state

# Import Pydantic model for AG-UI support
from state import Section

@tool
def WriteSection(title: str, content: str, section_number: int, footer: str = ""): # pylint: disable=invalid-name,unused-argument
    """Write a section with content and footer containing references"""

def generate_random_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

class SectionWriterInput(BaseModel):
    research_query: str = Field(description="The research query or topic for the section.")
    section_title: str = Field(description="The title of the specific section to write.")
    idx: int = Field(description="An index representing the order of this section (starting at 0")
    state: Optional[Dict] = Field(description="State of the research")


@tool("section_writer", args_schema=SectionWriterInput, return_direct=True)
async def section_writer(research_query, section_title, idx, state):
    """Writes a specific section of a research report based on the query, section title, and provided sources."""

    config = RunnableConfig()
    # Log search queries
    state["logs"] = state.get("logs", [])
    state["logs"].append({
        "message": f"📝 Writing the {section_title} section...",
        "done": False
    })
    await copilotkit_emit_state(config, state)

    section_id = generate_random_id()
    # Create Pydantic Section object for AG-UI
    section = Section(
        idx=idx,
        title=section_title,
        content="",
        footer=""
    )

    content_state = {
        "state_key": f"section_stream.content.{idx}.{section_id}.{section_title}",
        "tool": "WriteSection",
        "tool_argument": "content"
    }
    footer_state = {
        "state_key": f"section_stream.footer.{idx}.{section_id}.{section_title}",
        "tool": "WriteSection",
        "tool_argument": "footer"
    }

    config = copilotkit_customize_config(
        config,
        emit_intermediate_state=[content_state, footer_state]
    )

    outline = state.get("outline", {})
    sources = state.get("sources").values()
    # Check if section exists (handle both Section objects and dicts)
    existing_indices = [sec.idx if isinstance(sec, Section) else sec['idx'] for sec in state.get('sections', [])]
    section_exists = section.idx in existing_indices

    if not section_exists:
        # Define the system and user prompts
        prompt = [{
            "role": "system",
            "content": (
                "You are an AI assistant that writes specific sections of research reports in markdown format. "
                "You must use the write_section tool to write the section content. "
                "Use all appropriate markdown features for academic writing, including but not limited to:\n\n"
                "- do NOT include the title of the section in markdown\n"
                "- Headers (# through ######)\n"
                "- Text formatting (*italic*, **bold**, ***bold italic***, ~~strikethrough~~)\n"
                "- Lists (ordered and unordered, with proper nesting)\n"
                "- Block quotes and nested blockquotes\n"
                "- Code blocks for technical content\n"
                "- Tables for structured data\n"
                "- Links [text](url)\n"
                "- Images ![alt text](url)\n"
                "- Footnote/footer/references [^1] with proper markdown formatting\n"
                "- Mathematical equations using LaTeX syntax ($inline$ and $$block$$)\n\n"
                "Format the content professionally with appropriate spacing and structure for academic papers:\n"
                "- Add blank lines before and after headers\n"
                "- Add blank lines before and after lists\n"
                "- Add blank lines before and after blockquotes\n"
                "- Add blank lines before and after code blocks\n"
                "- Add blank lines before and after tables\n"
                "- Add blank lines before and after math blocks\n\n"
                "IMPORTANT RULES FOR REFERENCES:\n\n"
                "1. Footnotes are only required when the section content references external sources or needs citations\n"
                "2. If footnotes exist, they must be section-specific and start from [^1] in each section\n" 
                "3. The same source may have different reference numbers in different sections\n"
                "4. All references must be placed in the footer field, not in the content\n"
                "5. Do not add separation lines between content and references\n"
                "6. Format references as a list, with each reference on a new line starting with [^n]:\n\n"
                "   [^1]: First reference\n"
                "   [^2]: Second reference\n"
                "   etc."
            )
        }, {
            "role": "user",
            "content": (
                f"Today's date is {datetime.now().strftime('%d/%m/%Y')}.\n\n"
                f"Research Query: {research_query}\n\n" 
                f"Section Title: {section_title}\n\n"
                f"Section Number: {idx}\n\n"
                f"Sources:\n{sources}\n\n"
                "Write a section using the write_section tool. The section should be detailed and well-structured in markdown. "
                "Use appropriate markdown formatting to create a professional academic document. "
                "Only use footnotes when citing sources or referencing external material. "
                "If footnotes are used, they must start from [^1] in this section. "
                "References must be defined in the footer field, not in the content. Each reference should link to a source URL."
            )
        }]
    else:
        # get the current content of the section we want to update
        current_section_state = state['sections'][section.idx]
        # Handle both Section objects and dicts
        current_title = current_section_state.title if isinstance(current_section_state, Section) else current_section_state['title']
        current_content = current_section_state.content if isinstance(current_section_state, Section) else current_section_state['content']
        current_footer = current_section_state.footer if isinstance(current_section_state, Section) else current_section_state['footer']

        # Extract and sanitize the last human message
        # Note: state['messages'] is converted to a dict format in tool_node
        user_request = ""
        if isinstance(state['messages'], dict):
            # Get the last human message from the dict format
            human_messages = [msg for msg_type, msg in state['messages'].items() if msg_type == 'HumanMessage']
            if human_messages:
                user_request = str(human_messages[-1])
        
        # Sanitize and truncate user request to prevent prompt injection
        # Remove any attempt to inject system instructions
        user_request = user_request.replace("</s>", "").replace("<|im_end|>", "").replace("<|endoftext|>", "")
        # Truncate to reasonable length (e.g., 2000 characters)
        max_length = 2000
        if len(user_request) > max_length:
            user_request = user_request[:max_length] + "...[truncated]"

        prompt = [{
            "role": "system",
            "content": (
                "You are an AI assistant that makes changes to a given section of a research report in markdown format. "
                "Use the given section and only make changes that were requested by the user. "
                "Do not change the title of a section unless explicitly requested by the user.\n\n"
                "The given section:\n"
                f"Title: {current_title}\n"
                f"Content: {current_content}\n"
                f"Footer: {current_footer}\n\n"
                "Now use the user's request to alter the given section.\n"
                f"The user request: {user_request}"
            )
        }, {
            "role": "user",
            "content": (
                "You are an AI assistant that has completed the task of creating a specific section of a research report, now your primary goal is to make changes to the section to fit the users request. "
                "Edit the given section of the report using the write_section tool. Make sure to only make changes to the section that the user requested. "
                "Before making changes to the given section of the report identify the location (heading/subheading/bullet point/etc.) where the user's request needs to be placed in the report, and then only make changes to this location and keep everything else the same. "
                "Use appropriate markdown formatting to create a professional academic report section. "
                "Do not alter the format of the given section unless explicitly instructed by the user."
            )
        }]

    try:
        # Convert prompts for OpenAI API
        lc_messages = convert_openai_messages(prompt)

        # Invoke OpenAI's model with tool
        model = ChatOpenAI(model="gpt-4o-mini", max_retries=1)
        response = await model.bind_tools([WriteSection]).ainvoke(lc_messages, config)

        state["logs"][-1]["done"] = True
        await copilotkit_emit_state(config, state)

        ai_message = cast(AIMessage, response)
        if ai_message.tool_calls:
            if ai_message.tool_calls[0]["name"] == "WriteSection":
                # Update Pydantic Section object
                section.title = ai_message.tool_calls[0]["args"].get("title", section.title)
                section.content = ai_message.tool_calls[0]["args"].get("content", "")
                section.footer = ai_message.tool_calls[0]["args"].get("footer", "")

        if section_exists:
            state["sections"][section.idx] = section
        else:
            state["sections"].append(section)

        # Process each stream state
        stream_states = {
            "content": content_state,
            "footer": footer_state
        }

        for stream_type, stream_info in stream_states.items():
            if stream_info["state_key"] in state:
                state[stream_info["state_key"]] = None
        await copilotkit_emit_state(config, state)

        tool_msg = f"Wrote the {section_title} Section, idx: {idx}"

        return state, tool_msg
    except Exception as e:

        # Clear logs
        state["logs"] = []
        await copilotkit_emit_state(config, state)

        return state, f"Error generating section: {e}"
