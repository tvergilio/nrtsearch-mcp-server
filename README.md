# NRTSearch MCP Server

This project implements a Model Context Protocol (MCP) server that exposes the search functionality from NRTSearch to AI assistants and tools such as GitHub Copilot agent and Claude. It allows AI assistants to query your Lucene-based search indexes through natural language.

## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Installation](#installation)
4. [Development Setup](#development-setup)
5. [Configuration](#configuration)
6. [Usage](#usage)
   - [With VS Code and GitHub Copilot](#with-vs-code-and-github-copilot)
   - [With Claude Desktop](#with-claude-desktop)
7. [API Reference](#api-reference)
8. [Contributing](#contributing)
9. [License](#license)

## Overview

This MCP server acts as a bridge between AI assistants and your NRTSearch index, allowing AI assistants to:

- Query search indexes using natural language
- Get information about available indexes
- Retrieve document fields and structure
- Execute complex search queries with filtering, sorting, and faceting

## Project Structure

```
nrtsearch-mcp-server/
├── .gitignore               # Git ignore file
├── .vscode/                 # VS Code settings
│   └── settings.json        # VS Code settings including GitHub Copilot integration
├── LICENSE                  # License file
├── README.md                # Project documentation
├── claude_desktop_config.json  # Example Claude Desktop configuration
├── config.json              # Sample server configuration
├── pyproject.toml           # Python project metadata
├── requirements.txt         # Python dependencies
├── run_server.sh            # Script to run the server
├── setup.py                 # Setup script for pip install
├── nrtsearch_mcp/           # Main package
│   ├── __init__.py          # Package initialization
│   ├── config.py            # Configuration handling
│   ├── nrtsearch_api.py     # NRTSearch API client
│   ├── server.py            # MCP server implementation
│   └── tools/               # MCP tools implementation
│       ├── __init__.py      # Tools package initialization
│       ├── index.py         # Index-related tools
│       ├── search.py        # Search-related tools
│       └── utils.py         # Utility functions
└── tests/                   # Tests
    ├── __init__.py          # Test package initialization
    ├── resources/           # Test resources
    ├── test_server.py       # Server tests
    └── test_tools.py        # Tools tests
```

## Installation

1. Make sure you have Python 3.10+ installed.

2. Clone this repository:
   ```bash
   git clone https://github.com/tvergilio/nrtsearch-mcp-server.git
   cd nrtsearch-mcp-server
   ```

3. Set up a virtual environment:
   ```bash
   # Using standard Python tools
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   # Install required packages
   pip install httpx pydantic pytest fastapi uvicorn
   ```

### MCP Package Installation

This project requires the Model Context Protocol (MCP) package. You have two options:

1. **Install from GitHub**: The official MCP Python SDK is available on GitHub. You can install it with:
   
   ```bash
   # Using the provided install script
   bash install_mcp.sh
   
   # Or manually
   pip install git+https://github.com/modelcontextprotocol/python-sdk.git
   ```

2. **Install Claude Desktop**: The MCP package is also installed with Claude Desktop. You can download it from [https://claude.ai/downloads](https://claude.ai/downloads).

If neither option is available, the code includes a mock implementation that allows you to develop and test without the actual MCP package.

## Usage

### Quick Start

The easiest way to get started is to use the quickstart script:

```bash
./quickstart.sh
```

This script will:
1. Check if the MCP package is installed, and install it if needed
2. Install all other dependencies
3. Start the server

### With VS Code and GitHub Copilot

To integrate with VS Code and GitHub Copilot:

1. Make sure you have VS Code with GitHub Copilot installed.

2. Configure VS Code settings:
   - Open VS Code settings (File > Preferences > Settings)
   - Search for "Copilot: Advanced"
   - Add "nrtsearch-mcp" to the "Model Context Providers" list.
   
   Alternatively, this repository includes `.vscode/settings.json` with the necessary configuration.

3. Start the NRTSearch MCP server:
   ```bash
   # Using the quickstart script
   ./quickstart.sh
   
   # Or manually
   ./run_server.sh
   ```

4. In VS Code, open the command palette (Cmd/Ctrl+Shift+P) and run "GitHub Copilot: Start Agent Chat".

5. Now you can chat with GitHub Copilot and ask questions about your search indexes:
   - "What indexes are available?"
   - "Search for restaurant reviews with 5 stars"
   - "Get information about field types in the yelp_reviews index"

### With Claude Desktop

For Claude Desktop integration:

1. Install Claude Desktop from [https://claude.ai/downloads](https://claude.ai/downloads).

2. Configure Claude Desktop by updating `~/Library/Application Support/Claude/claude_desktop_config.json` (on macOS) or using the provided `claude_desktop_config.json` as a template:

   ```json
   {
     "mcpServers": {
       "nrtsearch-mcp": {
         "command": "python",
         "args": [
           "-m",
           "nrtsearch_mcp.server"
         ],
         "cwd": "/absolute/path/to/nrtsearch-mcp-server"
       }
     }
   }
   ```

3. Restart Claude Desktop and look for the "Search and tools" icon.

## Configuration

The MCP server is configured using a JSON file. By default, it looks for:

1. Path specified in the `NRTSEARCH_MCP_CONFIG` environment variable
2. `./config.json` in the current directory
3. `~/nrtsearch-mcp-config.json` in the user's home directory

You can also specify the config file path manually:

```bash
./run_server.sh --config /path/to/config.json
```

The configuration file has the following structure:

```json
{
  "nrtsearch_connection": {
    "host": "localhost",
    "port": 8000,
    "use_https": false
  },
  "indexes": [
    {
      "name": "yelp_reviews",
      "description": "Yelp reviews dataset",
      "fields": ["review_id", "business_id", "stars", "text"],
      "default_search_fields": ["text"]
    }
  ],
  "log_level": "INFO"
}
```

### Configuration Options

- **nrtsearch_connection**: Connection details for your NRTSearch server
  - **host**: Hostname or IP address
  - **port**: Port number
  - **use_https**: Whether to use HTTPS for connections

- **indexes**: List of indexes to expose through the MCP server
  - **name**: Index name
  - **description**: Human-readable description
  - **fields**: List of field names
  - **default_search_fields**: Fields to search by default

- **log_level**: Logging level (INFO, DEBUG, WARNING, ERROR)

## API Reference

The following MCP tools are available:

| Tool Name | Description | Parameters | Return Value |
|-----------|-------------|------------|--------------|
| `search_index` | Search an index with a natural language query | `index_name`, `query`, `top_hits` | Search results |
| `get_indexes` | List all available indexes | None | List of indexes |
| `get_index_info` | Get information about an index | `index_name` | Index metadata |
| `get_document_by_id` | Retrieve a document by ID | `index_name`, `doc_id` | Document data |
| `get_field_info` | Get information about fields in an index | `index_name` | Field definitions |
| `search_advanced` | Perform advanced search | `index_name`, `query`, `filters`, `fields`, `start_hit`, `top_hits` | Search results with facets |

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
| `get_index_info` | Get information about an index | `index_name` | Index metadata |
| `get_document_by_id` | Retrieve a document by ID | `index_name`, `doc_id` | Document data |
| `get_field_info` | Get information about fields in an index | `index_name` | Field definitions |
| `search_advanced` | Perform advanced search | `index_name`, `query`, `filters`, `fields`, `start_hit`, `top_hits` | Search results with facets |

## Next Steps

1. Set up the basic project structure
2. Implement the core MCP server functionality
3. Create the NRTSearch API interface
4. Implement the MCP tools
5. Configure VS Code integration
6. Test and refine
