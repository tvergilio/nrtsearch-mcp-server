import sys
import json

# This script simulates a raw MCP (Model Context Protocol) connection over stdio.
# It sends a JSON-RPC request to stdin and reads the response from stdout.
# To use: pipe this script to your MCP server if it supports stdio transport.

mcp_request = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/execute",
    "params": {
        "name": "nrtsearch/search",
        "arguments": {
            "indexName": "yelp_reviews_staging",
            "queryText": "text:\"best tacos\"",
            "topHits": 5
        }
    }
}

# Write the request to stdout (which should be piped to the MCP server's stdin)
sys.stdout.write(json.dumps(mcp_request) + "\n")
sys.stdout.flush()

# Read the response from stdin (which should be piped from the MCP server's stdout)
response = sys.stdin.readline()
print("MCP server response:")
print(response)
