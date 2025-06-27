"""
Utility functions for NRTSearch MCP tools.
"""

from typing import Any, Dict


def format_field_value(field_value: Dict[str, Any]) -> str:
    """
    Format a field value from the NRTSearch API response.
    
    The NRTSearch API returns field values in a nested structure where the actual
    value is contained in a type-specific key (e.g., textValue, floatValue, etc.)
    
    Args:
        field_value: Field value dictionary from the API response
        
    Returns:
        Formatted string representation of the field value
    """
    if not isinstance(field_value, dict):
        return str(field_value)
        
    actual_value = field_value.get("fieldValue", {})
    
    # Extract the correct type of value based on keys ending with "Value"
    for key, value in actual_value.items():
        if key.endswith("Value"):
            return str(value)
            
    # If no typed value is found, return the raw field value
    return str(field_value)


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to a maximum length and add ellipsis if needed.
    
    Args:
        text: Text to truncate
        max_length: Maximum length before truncation
        
    Returns:
        Truncated text with ellipsis if truncated
    """
    if len(text) <= max_length:
        return text
        
    return text[:max_length - 3] + "..."


def format_lucene_query(natural_query: str) -> str:
    """
    Convert a natural language query to a Lucene query format.
    
    This is a simple implementation that could be expanded with more sophisticated
    NL to query conversion in the future.
    
    Args:
        natural_query: Natural language query
        
    Returns:
        Query formatted for Lucene
    """
    # This is a very simple implementation - for real use cases,
    # you might want a more sophisticated conversion
    parts = natural_query.split()
    
    # Handle some basic operators
    lucene_query = []
    skip_next = False
    
    for i, part in enumerate(parts):
        if skip_next:
            skip_next = False
            continue
            
        if part.lower() == "and" and i > 0 and i < len(parts) - 1:
            lucene_query.append("AND")
            
        elif part.lower() == "or" and i > 0 and i < len(parts) - 1:
            lucene_query.append("OR")
            
        elif part.lower() == "not" and i < len(parts) - 1:
            lucene_query.append("NOT")
            
        else:
            # Escape special characters
            for char in [":", "+", "-", "&&", "||", "!", "(", ")", "{", "}", "[", "]", "^", "\"", "~", "*", "?", "\\"]:
                if char in part:
                    part = part.replace(char, f"\\{char}")
            lucene_query.append(part)
            
    return " ".join(lucene_query)
