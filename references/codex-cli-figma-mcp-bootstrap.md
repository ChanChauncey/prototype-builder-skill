# Codex CLI + Figma MCP Bootstrap

Use this procedure when the user requests Codex CLI setup and Figma MCP registration.

## Steps

1. Check CLI:

```powershell
codex --version
```

2. If `codex` is missing, install Codex CLI using the official installation path available in current environment.

3. Register Figma MCP:

```powershell
codex mcp add figma --url https://mcp.figma.com/mcp
```

4. Verify:

```powershell
codex mcp list
```

Expected: an entry named `figma` appears in MCP list.

## Failure Handling

1. If add command fails, capture stderr and exit code.
2. Retry once after confirming network and CLI availability.
3. If still failing, return exact command output and stop further MCP-dependent steps.
