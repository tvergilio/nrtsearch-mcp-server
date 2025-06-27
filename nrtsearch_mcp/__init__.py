"""
NRTSearch MCP Server - Model Context Protocol server for NRTSearch.

This package provides an MCP server implementation that exposes NRTSearch
functionality to AI assistants via the Model Context Protocol.
"""


from importlib.metadata import version as _version
__version__ = _version("nrtsearch-mcp")
from .tools import search
__all__ = ["__version__", "search"]
