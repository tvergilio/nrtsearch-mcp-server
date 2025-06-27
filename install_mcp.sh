#!/bin/bash

# This script installs the Model Context Protocol (MCP) Python SDK from the GitHub repository

echo "Installing the MCP Python SDK from GitHub..."
pip install git+https://github.com/modelcontextprotocol/python-sdk.git

if [ $? -eq 0 ]; then
    echo "MCP Python SDK has been successfully installed!"
    echo "You can now run the NRTSearch MCP server."
else
    echo "Failed to install the MCP Python SDK."
    echo "Please check your internet connection and try again."
    echo "Alternatively, you can use Claude Desktop which includes the MCP package."
    exit 1
fi
