# Handling MCP Import Errors

This guide explains how to handle the "Import 'mcp.server.fastmcp' could not be resolved" error that may appear in VS Code.

## Background

The NRTSearch MCP server requires the Model Context Protocol (MCP) package. While it's not available on PyPI, there are now multiple ways to obtain it:

1. **Install the official MCP Python SDK** from GitHub:
   ```bash
   pip install git+https://github.com/modelcontextprotocol/python-sdk.git
   ```

2. **Use Claude Desktop**, which includes the MCP package.

During development, you may see import errors for the MCP package if you don't have either of these installed.

## Solutions

### 0. Install the Official MCP Python SDK

The preferred solution is to install the official MCP Python SDK from GitHub:

```bash
pip install git+https://github.com/modelcontextprotocol/python-sdk.git
```

If you can't install the SDK, we've implemented several fallback solutions:

### 1. Type-Ignore Comments

The import statements include `# type: ignore` comments to suppress the specific import errors:

```python
from mcp.server.fastmcp import FastMCP  # type: ignore
```

### 2. Mock Implementation

The code includes a mock implementation of the FastMCP class that is used when the actual MCP package is not available:

```python
try:
    from mcp.server.fastmcp import FastMCP  # type: ignore
except ImportError:
    # Mock implementation for development without MCP package
    class FastMCP:
        """Mock FastMCP class for development without the actual package."""
        # ...implementation...
```

### 3. Stub Files

The repository includes stub files in the `stubs/` directory that provide type hints for the MCP package. These stubs are automatically included in the Python path for VS Code through the `.vscode/settings.json` configuration.

### 4. VS Code Configuration

The `.vscode/settings.json` file includes settings to:
- Ignore missing imports in Pylance
- Add the stubs directory to the Python path

```json
"python.analysis.diagnosticSeverityOverrides": {
  "reportMissingImports": "none"
},
"python.analysis.extraPaths": [
  "${workspaceFolder}/stubs"
]
```

### 5. MyPy Configuration

The `pyproject.toml` file includes mypy configuration to ignore missing imports for the MCP package:

```toml
[[tool.mypy.overrides]]
module = "mcp.*"
ignore_missing_imports = true
```

## What to Do When the MCP Package Is Available

When you have the actual MCP package available (e.g., after installing the MCP Python SDK or Claude Desktop):

1. The try-except blocks will import the real package instead of the mock implementation
2. The stubs will be ignored in favor of the real package
3. You can remove the type-ignore comments if desired
