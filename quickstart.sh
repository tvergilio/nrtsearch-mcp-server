#!/bin/bash

# This script sets up and runs the NRTSearch MCP server with Python 3.10+ and HTTP transport

# Check if we have Python 3.10+ available
PYTHON_CMD=""
for cmd in python3.12 python3.11 python3.10; do
    if command -v $cmd &> /dev/null; then
        PYTHON_CMD=$cmd
        break
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "❌ Error: This script requires Python 3.10 or higher."
    echo "Please install Python 3.10+ and try again."
    exit 1
fi

echo "✅ Using Python: $($PYTHON_CMD --version)"

# Check if virtual environment exists, create if not
VENV_DIR=".venv_mcp"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    $PYTHON_CMD -m venv $VENV_DIR
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"
echo "✅ Activated virtual environment: $(which python)"
echo "Python version: $(python --version)"

# Check if the MCP package is installed
if python -c "import mcp" &> /dev/null; then
    echo "✅ MCP package is already installed."
else
    echo "❌ MCP package is not installed."
    echo "Installing the MCP Python SDK from GitHub..."
    pip install git+https://github.com/modelcontextprotocol/python-sdk.git
    
    if [ $? -ne 0 ]; then
        echo "Failed to install the MCP Python SDK."
        echo "Please check your internet connection and try again."
        exit 1
    else
        echo "✅ MCP Python SDK has been successfully installed!"
    fi
fi

# Install other dependencies
echo "Checking and installing dependencies..."
pip install httpx pydantic pytest

# Set environment variables for the server
export MCP_PORT=3000
export MCP_HOST="127.0.0.1"
SERVER_URL="http://$MCP_HOST:$MCP_PORT"

# Print instructions for VS Code integration
echo ""
echo "========================================================"
echo "🔔 IMPORTANT: VS CODE INTEGRATION INSTRUCTIONS 🔔"
echo "========================================================"
echo "1. Make sure the server is running (this script will start it)"
echo "2. In VS Code, press Cmd+Shift+P (or Ctrl+Shift+P)"
echo "3. Type and select: MCP: Add Server"
echo "4. Enter the following information:"
echo "   - Name: nrtsearch-mcp"
echo "   - URL: $SERVER_URL"
echo "5. Wait for the connection to be established"
echo "6. You can now use GitHub Copilot to search your NRTSearch index"
echo "========================================================"
echo ""

# Start the server
echo "Starting the NRTSearch MCP server on $SERVER_URL..."
python -m nrtsearch_mcp.server -t http

echo "Server has been shut down."
