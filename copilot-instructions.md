# GitHub Copilot Instructions

## MCP Server Integration

You are configured to work with an NRTSearch MCP server running at http://localhost:8000. This server exposes search functionality through the MCP protocol.

### Available MCP Tools

The following tools are available through the MCP server:

- `search_index`: Search the Yelp reviews index using natural language queries
  - Parameters:
    - index_name: "yelp_reviews_staging"
    - query: The search query text
    - top_hits: Number of results to return (optional, default 10)

### How to Use

When asked to search or query the reviews:

1. The MCP server is already configured in VS Code settings under "mcp.servers.nrtsearch-mcp-server"
2. Use the MCP protocol to call the search_index tool directly
3. Process and display the results

### Example Queries

- "Find reviews mentioning great tacos"
- "Search for 5-star reviews of Italian restaurants"
- "Get the top 3 reviews about sushi"

### Important Notes

- Always use the MCP protocol directly, not HTTP/REST calls
- The server must be running locally on port 8000
- Queries should target the yelp_reviews_staging index by default
- Return results in a clear, formatted way

## Integration Rules

1. Always prefer using the MCP server's built-in tools over constructing HTTP requests
2. When searching, use the official MCP protocol interfaces
3. Check server availability before making queries
4. Handle responses appropriately and format them for user readability