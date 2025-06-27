## Contributing

Contributions are welcome! Here's how you can contribute to this project:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes
4. Add or update tests as necessary
5. Run the tests to make sure they pass
6. Submit a pull request

### Development Setup

1. Clone your fork of the repository
2. Set up the development environment:

```bash
# Using UV
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
# Install the MCP Python SDK
uv pip install git+https://github.com/modelcontextprotocol/python-sdk.git

# Or using standard pip
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
# Install the MCP Python SDK
pip install git+https://github.com/modelcontextprotocol/python-sdk.git

# Or use the install script
bash install_mcp.sh
```

3. Run the tests:

```bash
pytest
```

### Handling MCP Import Errors

The best way to avoid import errors is to install the official MCP Python SDK from GitHub as shown in the setup steps above.

If you can't install the SDK or prefer to use Claude Desktop's version, and you're using VS Code and see errors like "Import 'mcp.server.fastmcp' could not be resolved", see [IMPORT_ERRORS.md](IMPORT_ERRORS.md) for solutions. We've added several features to make development easier without the actual MCP package:

- Mock implementation of the FastMCP class
- Type stubs in the `stubs/` directory
- VS Code settings to ignore missing imports
- Type-ignore comments on import statements

### Code Style

This project uses:
- Black for code formatting
- isort for import sorting
- MyPy for type checking

You can run all of these with:

```bash
black nrtsearch_mcp tests
isort nrtsearch_mcp tests
mypy nrtsearch_mcp
```

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
