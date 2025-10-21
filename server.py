import os

# --- MUST come before importing fastmcp ---
os.environ["FASTMCP_TRANSPORT"] = "http"
port = int(os.getenv("PORT", 8080))
os.environ["FASTMCP_PORT"] = str(port)

import logging
from fastmcp import FastMCP, Context
from mcp.server.session import ServerSession
from tools.transaction_status import get_transaction_status_tool, TransactionStatusOutput

# Monkeypatch section
old__received_request = ServerSession._received_request
async def _received_request(self, *args, **kwargs):
    try:
        return await old__received_request(self, *args, **kwargs)
    except RuntimeError as e:
        if "Received request before initialization" in str(e):
            return None
        raise
ServerSession._received_request = _received_request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("felix-tools")

mcp = FastMCP("felix-tools")

@mcp.tool(
    name="get_transaction_status_v1",
    description="Fetch a user's previous transactions via their user_id.",
)
def register_transaction_status(user_id: str, ctx: Context) -> TransactionStatusOutput:
    result = get_transaction_status_tool(user_id)
    logger.info(f"Result: {result}")
    return result

if __name__ == "__main__":
    logger.info(f"Starting MCP HTTP server on port {port}...")
    mcp.run(transport="sse", host="0.0.0.0", port=port)
