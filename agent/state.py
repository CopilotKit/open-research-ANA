from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from typing import TypedDict, Dict, Union, List, Annotated, Optional
from pydantic import BaseModel, Field
from copilotkit import CopilotKitState # extends MessagesState


class ProposalSection(BaseModel):
    """A section in the research proposal."""
    title: str = Field(description="The title of the section")
    description: str = Field(description="A brief description of what this section will cover")
    approved: bool = Field(default=False, description="Whether this section has been approved by the user")


class Proposal(BaseModel):
    """The complete research proposal structure."""
    sections: Dict[str, ProposalSection] = Field(
        default_factory=dict,
        description="The sections of the research proposal"
    )
    remarks: Optional[str] = Field(
        default=None,
        description="Additional feedback or remarks from the user about the proposal"
    )
    approved: bool = Field(
        default=False,
        description="Whether the entire proposal has been approved"
    )


class Section(BaseModel):
    """A written section of the research report."""
    idx: int = Field(description="The index/order of the section")
    title: str = Field(description="The title of the section")
    content: str = Field(description="The content of the section")
    footer: str = Field(default="", description="Footer notes or citations for the section")


class Source(BaseModel):
    """A source used in the research."""
    url: str = Field(description="The URL of the source")
    title: str = Field(default="", description="The title of the source")
    score: float = Field(default=0.0, description="Relevance score of the source")


class Log(BaseModel):
    """A log entry for tracking research progress."""
    message: str = Field(description="The log message")
    status: str = Field(description="The status level (info, success, error, etc.)")


class ResearchState(CopilotKitState):
    """State for the research agent with AG-UI support."""
    title: str = Field(default="", description="The title of the research report")
    proposal: Optional[Proposal] = Field(
        default=None,
        description="The proposed structure before user approval"
    )
    outline: Dict[str, Dict[str, str]] = Field(
        default_factory=dict,
        description="The approved outline structure"
    )
    sections: List[Section] = Field(
        default_factory=list,
        description="The written sections of the report"
    )
    footnotes: str = Field(default="", description="Footnotes for the entire report")
    sources: Dict[str, Source] = Field(
        default_factory=dict,
        description="Sources used in the research"
    )
    tool: str = Field(default="", description="The current tool being used")
    logs: List[Log] = Field(
        default_factory=list,
        description="Progress logs to display in the frontend"
    )


