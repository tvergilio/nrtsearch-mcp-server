"""
Tests for the NRTSearch MCP server.
"""

import pytest
import pytest_asyncio

from nrtsearch_mcp.config import get_default_config
from nrtsearch_mcp.nrtsearch_api import NRTSearchClient


@pytest.fixture
def config():
    """Get default configuration for testing."""
    return get_default_config()


@pytest_asyncio.fixture
async def mock_client(monkeypatch):
    """Mock the NRTSearch client for testing."""
    
    class MockNRTSearchClient(NRTSearchClient):
        """Mock client that returns predefined responses."""
        
        async def _make_request(self, method, path, json_data=None):
            """Mock request method."""
            if path == "/indices":
                return {"indices": ["yelp_reviews", "test_index"]}
                
            elif path.startswith("/indices/"):
                index_name = path.split("/")[-1]
                if index_name == "yelp_reviews":
                    return {
                        "settings": {"numReplicas": 1},
                        "status": {"numDocs": 1000}
                    }
                    
            elif path == "/search":
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
                
            # Default empty response
            return {}
    
    return MockNRTSearchClient(config().nrtsearch_connection)


@pytest.mark.asyncio
async def test_get_indexes(mock_client):
    """Test getting indexes."""
    indexes = await mock_client.get_indexes()
    assert indexes == ["yelp_reviews", "test_index"]


@pytest.mark.asyncio
async def test_search(mock_client):
    """Test search functionality."""
    result = await mock_client.search("yelp_reviews", "restaurant")
    assert result.get("totalHits", {}).get("value") == 2
    assert len(result.get("hits", [])) == 2
    
    # Check first hit
    first_hit = result["hits"][0]
    assert first_hit["score"] == 0.9
    assert first_hit["fields"]["review_id"]["fieldValue"]["textValue"] == "abc123"
    assert first_hit["fields"]["text"]["fieldValue"]["textValue"] == "Great restaurant!"
    assert first_hit["fields"]["stars"]["fieldValue"]["floatValue"] == 5.0
