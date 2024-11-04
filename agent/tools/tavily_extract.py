from langchain_core.tools import tool
from pydantic import BaseModel, Field
from tavily import AsyncTavilyClient
from typing import List, Optional, Dict


tavily_client = AsyncTavilyClient()


class TavilyExtractInput(BaseModel):
    urls: List[str] = Field(description="list of a single or several URLs for extracting raw content to gather additional information")
    state: Optional[Dict] = Field(description="state of the search")


@tool("tavily_extract", args_schema=TavilyExtractInput, return_direct=True)
async def tavily_extract(urls, state):
    """Perform full scrape to a provided list of urls."""

    try:
        response = await tavily_client.extract(urls=urls)
        results = response['results']
        # match and add raw_content to urls in state
        tool_msg = "Extracted raw content to gather additional information from the following sources:\n"
        for url in results:
            state["sources"][url]["raw_content"] = results[url]["raw_content"]
            tool_msg += f"{url}\n"
        return state, tool_msg

    except Exception as e:
        print(f"Error occurred during extract: {str(e)}")
        return state, ""
