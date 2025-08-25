# Felix MCP

A Model Context Protocol (MCP) server that provides tools for interacting with various services and APIs.

## Overview

Felix MCP is a Python-based MCP server that implements the Model Context Protocol to provide structured tools for AI assistants and other applications. It currently includes tools for checking transaction status and can be easily extended with additional functionality.

## Features

- **MCP Server**: Implements the Model Context Protocol for standardized tool communication
- **Transaction Status Tool**: Check the status of transactions by ID
- **Extensible Architecture**: Easy to add new tools through the registry system
- **Schema Validation**: Input and output validation using Pydantic schemas

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd felix-mcp
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (if needed):
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Usage

### Running the Server

Start the MCP server:

```bash
python main.py
```

The server will start and communicate via stdio, making it compatible with MCP clients.

### Available Tools

#### Transaction Status Tool

- **Name**: `get_transaction_status@v1`
- **Description**: Fetch the status of a transaction by its ID
- **Input**: Transaction ID
- **Output**: Transaction status information

## Architecture

The project follows a modular architecture:

- `main.py` - Entry point and server initialization
- `mcp/mcp_server.py` - Core MCP server implementation
- `mcp/registry.py` - Tool registration system
- `mcp/tools/` - Individual tool implementations
  - Each tool has its own directory with schema, service, and tool files

## Adding New Tools

To add a new tool:

1. Create a new directory in `mcp/tools/`
2. Implement the tool's schema, service, and tool files
3. Use the `@register_tool` decorator to register it
4. The tool will automatically be available through the MCP server

