"""
Stub file for mcp.server.fastmcp to help with IDE integration.
"""

from typing import Any, Callable, List, Optional, TypeVar, Union, overload

# Type variables for the decorator pattern
F = TypeVar('F', bound=Callable[..., Any])
T = TypeVar('T')

class FastMCP:
    """
    FastMCP is the main class for the Model Context Protocol server.
    
    This stub implementation is for IDE integration and provides type hints
    for development without the actual MCP package.
    """
    
    def __init__(self, name: str):
        """
        Initialize a new FastMCP instance.
        
        Args:
            name: The name of the MCP server
        """
        self.name = name
        self.tools: List[Callable[..., Any]] = []
        
    def tool(self) -> Callable[[F], F]:
        """
        Decorator to register a function as an MCP tool.
        
        Returns:
            A decorator function that registers the decorated function as a tool
        """
        def decorator(func: F) -> F:
            self.tools.append(func)
            return func
        return decorator
    
    def run(self, 
            transport: str = "stdio", 
            host: Optional[str] = None, 
            port: Optional[int] = None) -> None:
        """
        Run the MCP server with the specified transport.
        
        Args:
            transport: Transport mechanism ("stdio" or "http")
            host: Host address for HTTP transport
            port: Port number for HTTP transport
        """
        pass
    
    def list_tools(self) -> List[Any]:
        """
        List all registered tools.
        
        Returns:
            A list of tool descriptors
        """
        return []
        
    async def invoke_tool(self, 
                         name: str, 
                         parameters: dict) -> Any:
        """
        Invoke a tool by name with the given parameters.
        
        Args:
            name: The name of the tool to invoke
            parameters: The parameters to pass to the tool
            
        Returns:
            The result of the tool invocation
        """
        pass
