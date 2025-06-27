# MCP Stubs

This directory contains stub files for the Model Context Protocol (MCP) package.
These stubs provide type hints for the MCP package, allowing IDE integrations like
VS Code with Pylance to provide code completion and type checking without the 
actual MCP package being installed.

**Note:** With the release of the official MCP Python SDK on GitHub, it's recommended
to install the SDK directly rather than relying on these stubs:

```bash
pip install git+https://github.com/modelcontextprotocol/python-sdk.git
```

These stubs are still provided as a fallback option for users who cannot install the SDK.

## Usage

These stubs are automatically included in the Python path for VS Code through
the `.vscode/settings.json` configuration.

For CLI type checking with mypy, these stubs are configured in the `pyproject.toml` file.

## Notes

- These stubs are for development purposes only and provide minimal functionality.
- When the actual MCP package is installed, these stubs will be overridden by the real package.
- The implementations here are based on observed behavior and documentation, but may not be 100% accurate.
