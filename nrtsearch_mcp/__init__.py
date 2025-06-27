"""
NRTSearch MCP Server - Model Context Protocol server for NRTSearch.

This package provides an MCP server implementation that exposes NRTSearch
functionality to AI assistants via the Model Context Protocol.
"""


try:
    from importlib.metadata import version as _version
    __version__ = _version("nrtsearch-mcp")
except Exception:
    __version__ = "0.0.0"
from .server import search
__all__ = ["__version__", "search"]
