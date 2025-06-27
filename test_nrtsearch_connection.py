#!/usr/bin/env python3
"""
Test script to check if the NRTSearch server is accessible.
"""

import asyncio
import httpx
import sys
import json

# Base URL for the NRTSearch server
BASE_URL = "http://localhost:8080"

async def test_connection():
    """Test connection to the NRTSearch server."""
    print(f"Testing connection to NRTSearch server at {BASE_URL}...")
    
    try:
        # Try to get the list of indices
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/v1/indices", timeout=5.0)
            
            if response.status_code == 200:
                indices = response.json()
                print("Successfully connected to NRTSearch server!")
                print(f"Available indices: {json.dumps(indices, indent=2)}")
                return True
            else:
                print(f"Error: Received status code {response.status_code}")
                print(f"Response: {response.text}")
                return False
    except Exception as e:
        print(f"Error connecting to NRTSearch server: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_connection())
    sys.exit(0 if result else 1)
