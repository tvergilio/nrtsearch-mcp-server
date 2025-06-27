#!/usr/bin/env python3
"""
Simple script to test the connection to NRTSearch.
"""

import sys
import json
import httpx

def test_nrtsearch_connection():
    """Test the connection to the NRTSearch server."""
    # Load the configuration
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return False
    
    host = config["nrtsearch_connection"]["host"]
    port = config["nrtsearch_connection"]["port"]
    use_https = config["nrtsearch_connection"]["use_https"]
    
    protocol = "https" if use_https else "http"
    base_url = f"{protocol}://{host}:{port}"
    
    # Try to connect to the server
    try:
        print(f"Connecting to NRTSearch at {base_url}...")
        response = httpx.get(f"{base_url}/", timeout=5.0)
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error connecting to NRTSearch: {e}")
        return False

if __name__ == "__main__":
    success = test_nrtsearch_connection()
    print(f"Connection test {'succeeded' if success else 'failed'}")
    sys.exit(0 if success else 1)
