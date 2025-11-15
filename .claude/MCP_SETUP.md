# CopilotKit VIBE CODING MCP Setup

This guide helps you set up the CopilotKit VIBE CODING MCP server for the CopilotKit Expert Plugin.

## What is VIBE CODING MCP?

The **VIBE CODING MCP** is CopilotKit's official Model Context Protocol server that provides:
- Real-time access to CopilotKit documentation
- Official code examples from CopilotKit repositories
- API references and best practices
- Version-specific guidance

## Setup Instructions

### Method 1: Using Claude CLI (Recommended)

Run this command in your terminal:

```bash
claude mcp add --transport sse copilotkit-mcp https://mcp.copilotkit.ai/sse
```

This will:
1. Add the CopilotKit MCP server to your Claude configuration
2. Configure it to use Server-Sent Events (SSE) transport
3. Make it available to all Claude Code sessions

### Method 2: Manual Configuration

If the CLI command doesn't work, manually configure the MCP:

1. **Locate your Claude config file**:
   - Linux/Mac: `~/.config/claude/config.json`
   - Windows: `%APPDATA%\claude\config.json`

2. **Add the MCP server**:

```json
{
  "mcpServers": {
    "copilotkit-mcp": {
      "url": "https://mcp.copilotkit.ai/sse",
      "transport": "sse"
    }
  }
}
```

3. **Restart Claude Code** to apply changes.

### Method 3: Environment Variable

Set an environment variable to configure the MCP:

```bash
export CLAUDE_MCP_COPILOTKIT_URL="https://mcp.copilotkit.ai/sse"
```

Add this to your `~/.bashrc`, `~/.zshrc`, or equivalent.

## Verification

To verify the MCP is configured correctly:

### Using Claude CLI

```bash
claude mcp list
```

You should see:
```
copilotkit-mcp (https://mcp.copilotkit.ai/sse) [sse]
```

### Testing in Claude Code

Ask Claude a CopilotKit question:

```
You: What is the latest version of CopilotKit?

Claude (should use MCP to fetch current info):
The latest version of CopilotKit is [version from MCP]...
```

## Troubleshooting

### Issue: MCP server not connecting

**Possible causes:**
1. Network/firewall blocking the URL
2. Incorrect URL or transport type
3. Claude config not reloaded

**Solutions:**

1. **Check network connectivity**:
```bash
curl -I https://mcp.copilotkit.ai/sse
```

Should return HTTP 200 OK.

2. **Verify transport type**:
The transport MUST be `sse` (Server-Sent Events), not `stdio`.

3. **Restart Claude Code**:
Close and reopen Claude Code after configuration changes.

### Issue: MCP server not showing in list

**Solution:**

1. Check config file syntax (valid JSON)
2. Ensure proper permissions on config file
3. Try removing and re-adding:

```bash
claude mcp remove copilotkit-mcp
claude mcp add --transport sse copilotkit-mcp https://mcp.copilotkit.ai/sse
```

### Issue: Plugin works but MCP not used

**Note:** The CopilotKit Expert Plugin works even WITHOUT MCP connection!

- **With MCP**: Gets latest docs, real-time API info
- **Without MCP**: Uses built-in knowledge (still very capable)

The MCP enhances the plugin but is not required.

## MCP Capabilities

Once configured, the MCP provides:

### 1. Documentation Search
```
/copilotkit-docs

> Search for "useCoAgent hook"
```

The MCP fetches the latest official documentation.

### 2. Code Examples
```
"Show me the official example of CoAgent state synchronization"
```

The MCP retrieves examples from CopilotKit's GitHub repos.

### 3. API References
```
"What are all the parameters for CopilotKitProvider?"
```

The MCP provides current API signatures.

### 4. Version Information
```
"What changed in CopilotKit v1.5.20?"
```

The MCP accesses version-specific changelogs.

## Using the MCP

### Implicit Usage

The CopilotKit Expert Plugin automatically uses the MCP when:
- You ask documentation questions
- You request code examples
- You search for API references
- You use `/copilotkit-docs` command

### Explicit Usage

You can explicitly request MCP usage:

```
"Use the VIBE CODING MCP to get the latest docs for useCoAgentStateRender"
```

## Alternative: Manual Documentation Access

If you can't configure the MCP, you can still:

1. **Reference built-in patterns**:
   - See `.claude/copilotkit-patterns.md`
   - Contains extensive examples and patterns

2. **Browse official docs manually**:
   - https://docs.copilotkit.ai/
   - Copy/paste relevant sections to Claude

3. **Use the expert agent**:
   - Still has deep CopilotKit knowledge
   - Can answer most questions without MCP

## Cloud vs Local

### Cloud (GitHub Codespaces, etc.)

MCP works seamlessly in cloud environments:
- SSE transport works over HTTP
- No local setup required
- Same command to configure

### Local Development

Works the same way:
- SSE transport is firewall-friendly
- No special network configuration
- Automatic reconnection

## Security & Privacy

The VIBE CODING MCP:
- ✅ Is official from CopilotKit
- ✅ Uses HTTPS (secure)
- ✅ Only fetches public documentation
- ✅ Doesn't send your code to the server
- ✅ Read-only access (no mutations)

Your code and private data never leave your environment.

## Additional MCP Servers

You can add other MCP servers alongside CopilotKit:

```bash
# Add filesystem access
claude mcp add --transport stdio filesystem npx -y @modelcontextprotocol/server-filesystem

# Add web search
claude mcp add --transport stdio brave-search npx -y @modelcontextprotocol/server-brave-search
```

All MCP servers work together and enhance Claude Code capabilities.

## Support

If you have issues with the VIBE CODING MCP:

1. **CopilotKit Discord**: https://discord.gg/copilotkit
2. **CopilotKit GitHub Issues**: https://github.com/CopilotKit/CopilotKit/issues
3. **Claude Code Issues**: https://github.com/anthropics/claude-code/issues

## Summary

**To set up the MCP:**
```bash
claude mcp add --transport sse copilotkit-mcp https://mcp.copilotkit.ai/sse
```

**To verify:**
```bash
claude mcp list
```

**To use:**
Just ask CopilotKit questions! The MCP activates automatically.

---

**The CopilotKit Expert Plugin works with or without MCP, but MCP provides the best experience!**
