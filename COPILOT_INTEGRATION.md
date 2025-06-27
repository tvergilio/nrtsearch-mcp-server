# Integration with GitHub Copilot

This document explains how to integrate the NRTSearch MCP server with GitHub Copilot in VS Code.

## Prerequisites

1. VS Code installed
2. GitHub Copilot extension installed and configured
3. NRTSearch MCP server installed and running

## Configuration Steps

### 1. Update VS Code Settings

You need to configure VS Code to use the NRTSearch MCP server as a model context provider for GitHub Copilot.

#### Option 1: Manual Configuration

1. Open VS Code settings (File > Preferences > Settings)
2. Search for "Copilot: Advanced"
3. In the "Model Context Providers" setting, add "nrtsearch-mcp"

#### Option 2: Use Provided Settings

This repository includes a `.vscode/settings.json` file with the necessary configuration:

```json
{
  "github.copilot.advanced": {
    "modelContextProviders": [
      "nrtsearch-mcp"
    ]
  }
}
```

### 2. Start the NRTSearch MCP Server

```bash
# Navigate to the nrtsearch-mcp-server directory
cd /path/to/nrtsearch-mcp-server

# Start the server
./run_server.sh
```

### 3. Use GitHub Copilot with NRTSearch Data

1. Open VS Code
2. Start a Copilot Agent Chat (From the command palette: "GitHub Copilot: Start Agent Chat")
3. Ask questions about your search indexes, for example:
   - "What indexes are available?"
   - "Search for restaurant reviews with 5 stars"
   - "Find reviews mentioning 'delicious' or 'amazing'"

## Troubleshooting

### Common Issues

1. **MCP server not detected**: Make sure the server is running and the VS Code settings are configured correctly.

2. **Connection issues**: Check if the server is running on the expected port and host.

3. **Copilot not using the MCP tools**: Sometimes GitHub Copilot needs a specific prompt to use the MCP tools. Try explicitly mentioning the search index in your query.

### Debugging

To see if the MCP server is correctly registered with GitHub Copilot, you can check:

1. VS Code Developer Tools (Help > Toggle Developer Tools)
2. Look for MCP-related messages in the console

## Examples

Here are some examples of questions you can ask GitHub Copilot once the integration is set up:

- "Show me the top 5 restaurant reviews with a rating of 5 stars"
- "What are all the available fields in the yelp_reviews index?"
- "Search for reviews containing the word 'terrible' and having a rating lower than 3"
- "Get statistics about the yelp_reviews index"
