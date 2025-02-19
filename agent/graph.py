import json
from datetime import datetime
from typing import Literal, cast
from dotenv import load_dotenv

from langchain_core.messages import AIMessage, SystemMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph
from langgraph.types import Command
from langchain_core.runnables import RunnableConfig
from copilotkit.langchain import copilotkit_emit_state, copilotkit_customize_config

from state import ResearchState
from config import Config
from tools.tavily_search import tavily_search
from tools.tavily_extract import tavily_extract
from tools.outline_writer import outline_writer
from tools.section_writer import section_writer

load_dotenv('.env')

cfg = Config()

class ResearchAgent:
    def __init__(self):
        """
        Initialize the ResearchAgent.
        """
        if cfg.DEBUG:
            print("**In __init__**")

        self._initialize_tools()
        self._build_workflow()

    def _initialize_tools(self):
        """
        Initialize the available tools and create a name-to-tool mapping.
        """
        if cfg.DEBUG:
            print("**In _initialize_tools**")

        self.tools = [tavily_search, tavily_extract, outline_writer, section_writer]
        self.tools_by_name = {tool.name: tool for tool in self.tools}

    def _build_workflow(self):
        """
        Build the workflow graph with nodes and edges.
        """
        workflow = StateGraph(ResearchState)
        
        # Add nodes
        workflow.add_node("call_model_node", self.call_model_node)
        workflow.add_node("tools_node", self.tool_node)
        workflow.add_node("ask_human_node", self.ask_human_node)
        workflow.add_node("process_feedback_node", self.process_feedback_node)

        # Define graph structure
        workflow.set_entry_point("call_model_node")
        workflow.set_finish_point("call_model_node")
        workflow.add_edge("tools_node", "call_model_node")
        workflow.add_edge("ask_human_node", "process_feedback_node")
        workflow.add_edge("process_feedback_node", "call_model_node")

        self.graph = workflow.compile(interrupt_after=['ask_human_node'])

    def _build_system_prompt(self, state: ResearchState) -> str:
        """
        Build the system prompt based on current state.
        """
        if cfg.DEBUG:
            print("**In _build_system_prompt**")

        outline = state.get("outline", {})
        sections = state.get("sections", [])
        proposal = state.get("proposal", {})
        
        # The LLM is only aware of what it is told. When we build the system prompt, we give
        # it context to the LangGraph state and various other pieces of information.
        prompt_parts = [
            f"Today's date is {datetime.now().strftime('%d/%m/%Y')}.",
            "You are an expert research assistant, dedicated to helping users create comprehensive, well-sourced research reports. Your primary goal is to assist the user in producing a polished, professional report tailored to their needs.\n\n"
            "When writing a report use the following research tools:\n"
            "1. Use the tavily_search tool to start the research and gather additional information from credible online sources when needed.\n"
            "2. Use the tavily_extract tool to extract additional content from relevant URLs.\n"
            "3. Use the outline_writer tool to analyze the gathered information and organize it into a clear, logical **outline proposal**. Break the content into meaningful sections that will guide the report structure. You must use the outline_writer EVERY time you need to write an outline for the report\n"
            "4. After EVERY time you use the outline_writer tool, YOU MUST use review_proposal tool.\n"
            f"5. Once **outline proposal** is approved use the section_writer tool to write ONLY the sections of the report based on the **Approved Outline**{':' + str([outline[section]['title'] for section in outline]) if outline else ''} generated from the review_proposal tool. Ensure the report is well-written, properly sourced, and easy to understand. Avoid responding with the text of the report directly, always use the section_writer tool for the final product.\n\n"
            "After using the section_writer tool, actively engage with the user to discuss next steps. **Do not summarize your completed work**, as the user has full access to the research progress.\n"
            "Instead of sharing details like generated outlines or reports, simply confirm the task is ready and ask for feedback or next steps. For example:\n"
            "'I have completed [..MAX additional 5 words]. Would you like me to [..MAX additional 5 words]?'\n\n"
            "When you have a proposal, you must only write the sections that are approved. If a section is not approved, you must not write it."
            "Your role is to provide support, maintain clear communication, and ensure the final report aligns with the user's expectations.\n\n"
        ]

        # If the proposal has remarks and no outline, we add the proposal to the prompt
        if proposal.get('remarks') and not outline:
            prompt_parts.append(
                f"**\nReviewed Proposal:**\n"
                f"Approved: {proposal['approved']}\n"
                f"Sections: {proposal['sections']}\n"
                f"User's feedback: {proposal['remarks']}"
                "You must use the outline_writer tool to create a new outline proposal that incorporates the user's feedback\n."
            )

        # If the outline is present, we add it to the prompt
        if outline:
            prompt_parts.append(
                f"### Current State of the Report\n"
                f"\n**Approved Outline**:\n{outline}\n\n"
            )

        # If the sections are present, we add them to the prompt
        if sections:
            report_content = "\n".join(
                f"section {section['idx']} : {section['title']}\n"
                f"content : {section['content']}"
                f"footer : {section['footer']}\n"
                for section in sections
            )
            prompt_parts.append(f"**Report**:\n\n{report_content}")

        return "\n".join(prompt_parts)

    async def call_model_node(self, state: ResearchState, config: RunnableConfig) -> Command[Literal["tools_node", "ask_human_node", "__end__"]]:
        """
        Node for calling the model and handling the system prompt, messages, state, and tool bindings.
        """
        if cfg.DEBUG:
            print("**In call_model_node**")

        # Ensure last message is of correct type
        last_message = state['messages'][-1]
        if not isinstance(last_message, (AIMessage, SystemMessage, HumanMessage, ToolMessage)):
            last_message = HumanMessage(content=last_message.content)
            state['messages'][-1] = last_message

        prompt = self._build_system_prompt(state)
        
        # Call LLM
        response = await cfg.FACTUAL_LLM.bind_tools(
            self.tools + state.get("copilotkit", {}).get("actions", []),
            parallel_tool_calls=False
        ).ainvoke([
            SystemMessage(content=prompt),
            *state["messages"],
        ], config)

        response = cast(AIMessage, response)

        # Route based on tool calls
        if response.tool_calls:
            cpk_actions = state.get("copilotkit", {}).get("actions", [])
            if any(action.get("name") == tool_call.get("name") for action in cpk_actions 
                  for tool_call in response.tool_calls):
                return Command(goto="ask_human_node", update={"messages": response})
            return Command(goto="tools_node", update={"messages": response})

        return Command(goto="__end__", update={"messages": response})

    async def tool_node(self, state: ResearchState, config: RunnableConfig):
        """
        Custom asynchronous tool node that can access and update agent state. This is necessary
        because tools cannot access or update state directly.
        """
        if cfg.DEBUG:
            print("**In tool_node**")

        config = copilotkit_customize_config(config, emit_messages=False)

        msgs = []
        tool_state = {}
        for tool_call in state["messages"][-1].tool_calls:
            tool = self.tools_by_name[tool_call["name"]]
            # Temporary messages struct that are accessible only to tools.
            state['messages'] = {'HumanMessage' if type(message) == HumanMessage else 'AIMessage' : message.content for message in state['messages']}
            tool_call["args"]["state"] = state  # update the state so the tool could access the state
            new_state, tool_msg = await tool.ainvoke(tool_call["args"])
            tool_call["args"]["state"] = None
            msgs.append(ToolMessage(content=tool_msg, name=tool_call["name"], tool_call_id=tool_call["id"]))
            tool_state = {
                "title": new_state.get("title", ""),
                "outline": new_state.get("outline", {}),
                "sections": new_state.get("sections", []),
                "sources": new_state.get("sources", {}),
                "proposal": new_state.get("proposal", {}),
                "logs": new_state.get("logs", []),
                "tool": new_state.get("tool", {}),
                "messages": msgs
            }
            await copilotkit_emit_state(config, tool_state)

        return tool_state


    @staticmethod
    def ask_human_node(state: ResearchState):
        """
        Define an empty node to ask human for feedback via frontend tools.
        """
        if cfg.DEBUG:
            print("**In ask_human_node** waiting for human feedback from frontend")
        pass

    @staticmethod
    async def process_feedback_node(state: ResearchState, config: RunnableConfig):
        """
        Node for processing the user's response acquired in the ask_human_node.
        """
        if cfg.DEBUG:
            print("**In process_feedback_node**")

        # Process human feedback from frontend
        config = copilotkit_customize_config(
            config,
            emit_messages=True,  # make sure to enable emitting messages to the frontend
        )

        last_tool_message = cast(ToolMessage, state["messages"][-1])
        if cfg.DEBUG:
            print("**In process_feedback_node** received human feedback:\n",last_tool_message)

        # If the last tool message is 'review proposal', we need to update the proposal
        if last_tool_message.name == 'review_proposal':
            reviewed_proposal = json.loads(last_tool_message.content) # proposal will be a json object
            if reviewed_proposal.get("approved"):
                # Update outline with approved sections
                outline = {k: {'title': v['title'], 'description': v['description']} for k, v in
                           reviewed_proposal.get("sections", {}).items()
                           if isinstance(v, dict) and v.get('approved')}

                if cfg.DEBUG:
                    print("**In process_feedback_node** setting outline: {}".format(outline))

                state['outline'] = outline

            # Update proposal
            state["proposal"] = reviewed_proposal

        return state

graph = ResearchAgent().graph
