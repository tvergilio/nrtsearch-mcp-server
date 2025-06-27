"""
Tests for NRTSearch MCP tools.
"""

import pytest
import pytest_asyncio

from mcp.server.fastmcp import FastMCP

from nrtsearch_mcp.config import get_default_config
from nrtsearch_mcp.tools.search import register_search_tools
from nrtsearch_mcp.tools.index import register_index_tools


@pytest.fixture
def mock_client(monkeypatch):
    """Mock the NRTSearch client for testing."""
    
    class MockClient:
        """Mock client with predefined responses."""
        
        async def search(self, index_name, query, **kwargs):
            """Mock search method."""
            return {
                "totalHits": {"value": 2, "relation": "EQUAL_TO"},
                "hits": [
                    {
                        "luceneDocId": 123,
                        "score": 0.9,
                        "fields": {
                            "review_id": {
                                "fieldValue": {"textValue": "abc123"}
                            },
                            "text": {
                                "fieldValue": {"textValue": "Great restaurant!"}
                            },
                            "stars": {
                                "fieldValue": {"floatValue": 5.0}
                            }
                        }
                    },
                    {
                        "luceneDocId": 456,
                        "score": 0.8,
                        "fields": {
                            "review_id": {
                                "fieldValue": {"textValue": "def456"}
                            },
                            "text": {
                                "fieldValue": {"textValue": "Good food."}
                            },
                            "stars": {
                                "fieldValue": {"floatValue": 4.0}
                            }
                        }
                    }
                ]
            }
        
        async def get_indexes(self):
            """Mock get_indexes method."""
            return ["yelp_reviews", "test_index"]
        
        async def get_index_info(self, index_name):
            """Mock get_index_info method."""
            return {
                "settings": {"numReplicas": 1},
                "status": {"numDocs": 1000}
            }
        
        async def get_document(self, index_name, doc_id):
            """Mock get_document method."""
            return {
                "fields": {
                    "review_id": {
                        "fieldValue": {"textValue": doc_id}
                    },
                    "text": {
                        "fieldValue": {"textValue": "Sample review text"}
                    },
                    "stars": {
                        "fieldValue": {"floatValue": 5.0}
                    }
                }
            }
        
        async def get_field_info(self, index_name):
            """Mock get_field_info method."""
            return [
                {
                    "name": "review_id",
                    "type": "string",
                    "properties": {"stored": True}
                },
                {
                    "name": "text",
                    "type": "text",
                    "properties": {"stored": True}
                },
                {
                    "name": "stars",
                    "type": "float",
                    "properties": {"stored": True}
                }
            ]
    
    return MockClient()


@pytest.fixture
def mcp_instance():
    """Create a FastMCP instance for testing."""
    return FastMCP("test")


@pytest_asyncio.fixture
async def setup_tools(mcp_instance, mock_client):
    """Set up MCP tools for testing."""
    register_search_tools(mcp_instance, mock_client)
    register_index_tools(mcp_instance, mock_client)
    return mcp_instance


@pytest.mark.asyncio
async def test_search_index_tool(setup_tools):
    """Test the search_index tool."""
    mcp = setup_tools
    
    # Find the search_index tool
    search_tool = next(
        tool for tool in mcp.list_tools() if tool.name == "search_index"
    )
    
    # Call the tool
    result = await mcp.invoke_tool(
        search_tool.name,
        {"index_name": "yelp_reviews", "query": "restaurant", "top_hits": 5}
    )
    
    # Check the result
    assert isinstance(result, str)
    assert "Found 2 results" in result
    assert "Great restaurant!" in result
    assert "Good food" in result


@pytest.mark.asyncio
async def test_get_indexes_tool(setup_tools):
    """Test the get_indexes tool."""
    mcp = setup_tools
    
    # Find the get_indexes tool
    tool = next(
        tool for tool in mcp.list_tools() if tool.name == "get_indexes"
    )
    
    # Call the tool
    result = await mcp.invoke_tool(tool.name, {})
    
    # Check the result
    assert isinstance(result, str)
    assert "yelp_reviews" in result
    assert "test_index" in result


@pytest.mark.asyncio
async def test_get_index_info_tool(setup_tools):
    """Test the get_index_info tool."""
    mcp = setup_tools
    
    # Find the get_index_info tool
    tool = next(
        tool for tool in mcp.list_tools() if tool.name == "get_index_info"
    )
    
    # Call the tool
    result = await mcp.invoke_tool(
        tool.name,
        {"index_name": "yelp_reviews"}
    )
    
    # Check the result
    assert isinstance(result, str)
    assert "Index: yelp_reviews" in result
    assert "numReplicas: 1" in result
    assert "numDocs: 1000" in result
