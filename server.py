import logging
from mcp.server.session import ServerSession

# --- Temporary monkeypatch to avoid 'Received request before initialization' errors ---
old__received_request = ServerSession._received_request

async def _received_request(self, *args, **kwargs):
    try:
        return await old__received_request(self, *args, **kwargs)
    except RuntimeError as e:
        if "Received request before initialization" in str(e):
            # Silently ignore the premature request instead of crashing
            return None
        raise

ServerSession._received_request = _received_request
# -------------------------------------------------------------------------------

from fastmcp import FastMCP, Context
from tools.transaction_status import (
    get_transaction_status_tool,
    TransactionStatusOutput,
)

# --- Logging setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    force=True,
)
logger = logging.getLogger("felix-tools")

# --- Initialize FastMCP server ---
mcp = FastMCP("felix-tools")

# --- Tool definition ---
@mcp.tool(
    name="get_transaction_status_v1",
    description="Fetch a user's previous transactions via their user_id.",
)
def register_transaction_status(user_id: str, ctx: Context) -> TransactionStatusOutput:
    logger.info("=== MCP tool invoked ===")
    try:
        logger.info(f"Headers: {ctx.request.headers}")
    except AttributeError:
        if hasattr(ctx, "http"):
            logger.info(f"Headers: {getattr(ctx.http, 'headers', {})}")
        elif hasattr(ctx, "get_http_headers"):
            logger.info(f"Headers: {ctx.get_http_headers()}")

    result = get_transaction_status_tool(user_id)
    logger.info(f"Result: {result}")
    logger.info("========================")
    return result

# --- Entry point ---
if __name__ == "__main__":
    mcp.run()
