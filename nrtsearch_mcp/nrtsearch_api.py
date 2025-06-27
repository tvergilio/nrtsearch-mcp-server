"""
NRTSearch API client implementation.

This module provides a client interface to interact with the NRTSearch server.
"""

import json
import logging
from typing import Any, Dict, List, Optional, Union

import httpx

from nrtsearch_mcp.config import NRTSearchConnection

logger = logging.getLogger(__name__)


class NRTSearchClient:
    """Client for interacting with the NRTSearch server."""
    
    def __init__(self, connection: NRTSearchConnection):
        """Initialize the NRTSearch client.
        
        Args:
            connection: Connection configuration for the NRTSearch server
        """
        self.connection = connection
        self.base_url = connection.url
        
    async def _make_request(
        self, 
        method: str, 
        path: str, 
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make an HTTP request to the NRTSearch server.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path
            json_data: Optional JSON data to send
            
        Returns:
            Parsed JSON response
            
        Raises:
            httpx.HTTPError: If the request fails
        """
        url = f"{self.base_url}{path}"
        
        logger.debug(f"Making {method} request to {url}")
        if json_data:
            logger.debug(f"Request data: {json_data}")
        
        async with httpx.AsyncClient() as client:
            if method.upper() == "GET":
                response = await client.get(url, timeout=30.0)
            else:
                response = await client.post(url, json=json_data, timeout=30.0)
            
            response.raise_for_status()
            result = response.json()
            
            logger.debug(f"Response: {result}")
            return result
    
    async def search(
        self,
        index_name: str,
        query: str,
        start_hit: int = 0,
        top_hits: int = 10,
        retrieve_fields: Optional[List[str]] = None,
        filter_queries: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Search an index with the given query.
        
        Args:
            index_name: Name of the index to search
            query: Query text (can be in Lucene query syntax)
            start_hit: Starting position for results (for pagination)
            top_hits: Number of results to return
            retrieve_fields: List of fields to retrieve from matching documents
            filter_queries: Additional filter queries to apply
            
        Returns:
            Search results with hits and metadata
        """
        search_request = {
            "indexName": index_name,
            "queryText": query,
            "startHit": start_hit,
            "topHits": top_hits
        }
        
        if retrieve_fields:
            search_request["retrieveFields"] = retrieve_fields
            
        if filter_queries:
            search_request["filterQueries"] = filter_queries
            
        return await self._make_request("POST", "/search", search_request)
    
    async def get_indexes(self) -> List[str]:
        """Get a list of available indexes.
        
        Returns:
            List of index names
        """
        result = await self._make_request("GET", "/indices")
        return result.get("indices", [])
    
    async def get_index_info(self, index_name: str) -> Dict[str, Any]:
        """Get information about a specific index.
        
        Args:
            index_name: Name of the index to get information for
            
        Returns:
            Index metadata and configuration
        """
        return await self._make_request("GET", f"/indices/{index_name}")
    
    async def get_document(self, index_name: str, doc_id: str) -> Dict[str, Any]:
        """Retrieve a document by ID.
        
        Args:
            index_name: Name of the index to get the document from
            doc_id: Document ID
            
        Returns:
            Document data
        """
        return await self._make_request(
            "POST", 
            "/getDoc", 
            {"indexName": index_name, "docId": doc_id}
        )
    
    async def get_field_info(self, index_name: str) -> List[Dict[str, Any]]:
        """Get information about fields in an index.
        
        Args:
            index_name: Name of the index to get field info for
            
        Returns:
            List of field definitions
        """
        result = await self._make_request("GET", f"/indices/{index_name}/fields")
        return result.get("fields", [])
