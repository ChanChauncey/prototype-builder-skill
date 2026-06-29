# Figma Bridge MCP Config

Use this procedure when the user requests Figma MCP configuration for prototype restoration.

## Steps

1. Do not auto-install Codex CLI or any MCP package for the user.

2. Ask user to add this MCP config entry:

```json
{
  "figma-bridge": {
    "command": "npx",
    "args": ["-y", "@gethopp/figma-mcp-bridge"]
  }
}
```

3. Confirm an MCP entry named `figma-bridge` is available in current runtime.

4. For Figma link tasks, call `get_design_context` on selected node/page before any visual reconstruction.

## Failure Handling

1. If `figma-bridge` is unavailable, return exact blocking reason.
2. Do not run fallback auto-install commands.
3. Stop MCP-dependent restoration until configuration is fixed.
