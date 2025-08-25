from dotenv import load_dotenv
load_dotenv()

import asyncio
import mcp.server.stdio
from mcp.server.models import InitializationOptions
from mcp.server.lowlevel import NotificationOptions
from mcp.mcp_server import build_server

async def main():
    app = build_server()
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="felix-tools",
                server_version="0.1.0",
                capabilities=app.get_capabilities(notification_options=NotificationOptions())
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
