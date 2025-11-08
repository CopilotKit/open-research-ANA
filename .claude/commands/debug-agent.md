---
description: Debug issues with the LangGraph agent
---

Debug and troubleshoot issues with the LangGraph agent.

## Debugging Workflow:

1. **Check agent logs**:
   - Look for recent agent output
   - Identify error messages or stack traces
   - Note which node/tool failed

2. **Verify configuration**:
   - Check `agent/config.py` for correct model setup
   - Verify `agent/.env` has valid API keys
   - Ensure `agent/langgraph.json` is correct

3. **Test agent state**:
   - Check if state is being properly updated
   - Verify state schema in `agent/state.py`
   - Look for state serialization issues

4. **Inspect tool execution**:
   - Check which tool is causing issues
   - Test tool independently if possible
   - Verify tool inputs match expected schema

5. **Review system prompt**:
   - Check if system prompt is properly constructed
   - Verify state context is included
   - Ensure instructions are clear

6. **Common issues**:
   - **Tool not found**: Check if tool is registered in `self.tools`
   - **State update fails**: Verify state schema matches
   - **LLM doesn't call tools**: Review system prompt and tool descriptions
   - **Interrupt not working**: Check `process_feedback_node` implementation
   - **Tavily API errors**: Verify API key and rate limits

7. **LangSmith debugging**:
   - Suggest checking LangSmith trace for execution flow
   - Provide LangSmith URL if available

Provide specific recommendations based on the error pattern identified.
