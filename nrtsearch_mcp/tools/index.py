"""
Index-related MCP tools for NRTSearch.
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


def register_index_tools(mcp: FastMCP, client: NRTSearchClient) -> None:
    """Register all index-related tools with the MCP server.
    
    Args:
        mcp: The MCP server instance
        client: The NRTSearch client
    """
    
    @mcp.tool()
    async def get_indexes() -> str:
        """
        List all available indexes.
        
        Returns:
            List of available indexes and descriptions
        """
        try:
            indexes = await client.get_indexes()
            
            if not indexes:
                return "No indexes available."
                
            return "\n".join([f"- {index}" for index in indexes])
            
        except Exception as e:
            return f"Error retrieving indexes: {str(e)}"
    
    @mcp.tool()
    async def get_index_info(index_name: str) -> str:
        """
        Get detailed information about a specific index.
        
        Args:
            index_name: Name of the index to get information for
            
        Returns:
            Detailed index information
        """
        try:
            info = await client.get_index_info(index_name)
            
            # Format the index information
            formatted_info = f"Index: {index_name}\n\n"
            
            # Add settings information
            settings = info.get("settings", {})
            formatted_info += "Settings:\n"
            for key, value in settings.items():
                formatted_info += f"  {key}: {value}\n"
            
            # Add status information
            status = info.get("status", {})
            formatted_info += "\nStatus:\n"
            for key, value in status.items():
                formatted_info += f"  {key}: {value}\n"
                
            return formatted_info
            
        except Exception as e:
            return f"Error retrieving index information: {str(e)}"
    
    @mcp.tool()
    async def get_document_by_id(index_name: str, doc_id: str) -> str:
        """
        Retrieve a specific document by ID.
        
        Args:
            index_name: Name of the index to get the document from
            doc_id: Document ID
            
        Returns:
            Document content
        """
        try:
            doc = await client.get_document(index_name, doc_id)
            
            # Format the document data
            formatted_doc = f"Document {doc_id} from index {index_name}:\n\n"
            
            # Format fields
            fields = doc.get("fields", {})
            for field_name, field_value in fields.items():
                actual_value = field_value.get("fieldValue", {})
                
                # Extract the correct type of value
                value_type_keys = [k for k in actual_value.keys() if k.endswith("Value")]
                if value_type_keys:
                    value = actual_value.get(value_type_keys[0])
                    formatted_doc += f"{field_name}: {value}\n"
                
            return formatted_doc
            
        except Exception as e:
            return f"Error retrieving document: {str(e)}"
    
    @mcp.tool()
    async def get_field_info(index_name: str) -> str:
        """
        Get information about fields in an index.
        
        Args:
            index_name: Name of the index to get field info for
            
        Returns:
            Field definitions and types
        """
        try:
            fields = await client.get_field_info(index_name)
            
            if not fields:
                return f"No field definitions found for index '{index_name}'."
                
            # Format the field information
            formatted_fields = f"Fields for index {index_name}:\n\n"
            
            for field in fields:
                field_name = field.get("name", "unknown")
                field_type = field.get("type", "unknown")
                formatted_fields += f"- {field_name} ({field_type})\n"
                
                # Add additional field properties if available
                properties = field.get("properties", {})
                if properties:
                    for prop_name, prop_value in properties.items():
                        formatted_fields += f"  - {prop_name}: {prop_value}\n"
                    
            return formatted_fields
            
        except Exception as e:
            return f"Error retrieving field information: {str(e)}"
