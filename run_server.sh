#!/usr/bin/env bash
# Simple helper to start the MCP server on 127.0.0.1:3000
uvicorn nrtsearch_mcp.server:app --host 127.0.0.1 --port 3000
