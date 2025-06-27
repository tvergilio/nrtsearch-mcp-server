
# NRTSearch MCP Server

**Production-ready Model Context Protocol (MCP) server for Lucene/NRTSearch, with first-class support for AI assistants like GitHub Copilot and Claude.**

---

## Features

- Exposes NRTSearch/Lucene search as a robust MCP server for AI tools
- Accepts any Lucene query (Boolean, phrase, range, wildcard, fuzzy, etc.)
- Structured logging, retries, and highlight support
- Pure unit-testable search logic with full test coverage
- Easy integration with GitHub Copilot, Claude Desktop, and other MCP clients
- Modern Python packaging and configuration (Pydantic, pyproject.toml)

---

## Quick Start

```bash
git clone https://github.com/tvergilio/nrtsearch-mcp-server.git
cd nrtsearch-mcp-server
./quickstart.sh
```

This will:
- Install all dependencies (including MCP SDK)
- Start the server on the configured port

---


## Usage

### CLI / Manual

After installation, you can start the server with either:

```bash
# Using the Python module
python -m nrtsearch_mcp.server
```

### With GitHub Copilot (VS Code)
1. Install VS Code and GitHub Copilot
2. Add `nrtsearch-mcp` as a Model Context Provider in VS Code settings (see `.vscode/settings.json`)
3. Start the server (`./quickstart.sh` or `nrtsearch-mcp-server`)
4. Use Copilot Chat to query your Lucene indexes in natural language

---

## Configuration

The server is configured via environment variables and/or a JSON config file. By default, it looks for:
- `NRTSEARCH_MCP_CONFIG` env var (path to config)
- `./config.json` in the current directory
- `~/nrtsearch-mcp-config.json` in your home directory

Example config:
```json
{
  "nrtsearch_connection": {
    "host": "localhost",
    "port": 8000,
    "use_https": false
  },
  "log_level": "INFO"
}
```

Key environment variables:
- `LOG_LEVEL` (default: INFO)
- `NRTSEARCH_MCP_CONFIG` (optional config path)

---

## API: Search Tool

The main tool is `nrtsearch/search`:

**Parameters:**
- `index` (str): Index name (e.g. `yelp_reviews_staging`)
- `queryText` (str): Full Lucene query (e.g. `text:(irish AND pub AND (texas OR tx))`)
- `topHits` (int, default 10): Number of results (1-100)
- `retrieveFields` (list, optional): Fields to return (default: `["text", "stars"]`)
- `highlight` (bool, optional): Highlight matches

**Returns:**
- List of hits: `{score, stars, text}`

**Lucene Query Examples:**
- `text:(irish AND pub AND (texas OR tx))`
- `text:"great coffee"`
- `stars:[4 TO 5] AND text:(vegan AND brunch)`

---

## Testing

Run all tests (unit, no server needed):

```bash
pytest -v
```

Tests cover:
- Success, empty, and multiple hits
- Error handling (HTTP, network, malformed, missing fields)
- Retry logic
- Highlight and custom fields
- Input validation

---


## Project Structure

```
nrtsearch-mcp-server/
├── nrtsearch_mcp/
│   ├── server.py         # Main MCP server and search logic
│   ├── settings.py       # Pydantic config
│   └── ...
├── tests/               # Unit tests 
├── quickstart.sh        # One-step install & run
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Packaging/metadata
└── ...
```

---



## License

Apache License 2.0. See [LICENSE](LICENSE).
