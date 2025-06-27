"""
Search-related MCP tools for NRTSearch.
"""

from typing import Any, Dict, List, Optional

# Using try-except to handle when MCP package is not available
try:
    from mcp.server.fastmcp import FastMCP  # type: ignore
except ImportError:
    # Mock implementation for development without MCP package
    class FastMCP:
        """Mock FastMCP class for development without the actual package."""
        def __init__(self, name):
            self.name = name
            self.tools = []
            
        def tool(self):
            def decorator(func):
                self.tools.append(func)
                return func
            return decorator

from nrtsearch_mcp.nrtsearch_api import NRTSearchClient


def register_search_tools(mcp: FastMCP, client: NRTSearchClient) -> None:
    """Register all search-related tools with the MCP server.
    
    Args:
        mcp: The MCP server instance
        client: The NRTSearch client
    """
    
    @mcp.tool()
    async def search_index(index_name: str, query: str, top_hits: int = 10) -> str:
        """
        Search an index with a natural language query.
        
        Args:
            index_name: Name of the index to search
            query: Natural language query
            top_hits: Number of results to return (default: 10)
            
        Returns:
            Formatted search results
        """
        try:
            result = await client.search(
                index_name=index_name,
                query=query,
                top_hits=top_hits
            )
            
            # Format the results in a readable way
            hits = result.get("hits", [])
            total_hits = result.get("totalHits", {}).get("value", 0)
            
            if not hits:
                return f"No results found for query: '{query}'"
                
            formatted_results = f"Found {total_hits} results for query: '{query}'\n\n"
            
            for i, hit in enumerate(hits):
                formatted_results += f"Result {i+1} (Score: {hit.get('score', 0):.2f}):\n"
                
                # Format fields
                fields = hit.get("fields", {})
                for field_name, field_value in fields.items():
                    actual_value = field_value.get("fieldValue", {})
                    
                    # Extract the correct type of value
                    value_type_keys = [k for k in actual_value.keys() if k.endswith("Value")]
                    if value_type_keys:
                        value = actual_value.get(value_type_keys[0])
                        formatted_results += f"  {field_name}: {value}\n"
                
                formatted_results += "\n"
                
            return formatted_results
            
        except Exception as e:
            return f"Error searching index: {str(e)}"
    
    @mcp.tool()
    async def search_advanced(
        index_name: str, 
        query: str, 
        filters: Optional[List[str]] = None,
        fields: Optional[List[str]] = None,
        start_hit: int = 0,
        top_hits: int = 10
    ) -> str:
        """
        Perform an advanced search with filters and field selection.
        
        Args:
            index_name: Name of the index to search
            query: Search query (can use Lucene syntax)
            filters: Optional list of filter queries
            fields: Optional list of fields to retrieve
            start_hit: Starting position for results (for pagination)
            top_hits: Number of results to return
            
        Returns:
            Formatted search results
        """
        try:
            result = await client.search(
                index_name=index_name,
                query=query,
                start_hit=start_hit,
                top_hits=top_hits,
                retrieve_fields=fields,
                filter_queries=filters
            )
            
            # Format the results in a readable way
            hits = result.get("hits", [])
            total_hits = result.get("totalHits", {}).get("value", 0)
            
            if not hits:
                return f"No results found for query: '{query}'"
                
            formatted_results = f"Found {total_hits} results for query: '{query}'\n\n"
            
            for i, hit in enumerate(hits):
                formatted_results += f"Result {i+1} (Score: {hit.get('score', 0):.2f}):\n"
                
                # Format fields
                fields = hit.get("fields", {})
                for field_name, field_value in fields.items():
                    actual_value = field_value.get("fieldValue", {})
                    
                    # Extract the correct type of value
                    value_type_keys = [k for k in actual_value.keys() if k.endswith("Value")]
                    if value_type_keys:
                        value = actual_value.get(value_type_keys[0])
                        formatted_results += f"  {field_name}: {value}\n"
                
                formatted_results += "\n"
                
            return formatted_results
            
        except Exception as e:
            return f"Error performing advanced search: {str(e)}"
