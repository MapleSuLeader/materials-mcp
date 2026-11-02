#!/usr/bin/env python3
"""端到端自测：用 MCP 客户端走 stdio 握手 -> initialize -> tools/list -> tools/call."""
import asyncio
import json
import sys
import time

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

t0 = time.time()
SERVER = sys.executable


async def main() -> int:
    params = StdioServerParameters(command=SERVER, args=["server.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            init = await session.initialize()
            info = getattr(init, "server_info", None) or getattr(init, "serverInfo", None)
            sname = getattr(info, "name", None) or (info or {}).get("name")
            print(f"[1] handshake OK: server={sname} "
                  f"protocol={init.protocol_version if hasattr(init,'protocol_version') else init.protocolVersion}")
            tools = await session.list_tools()
            print(f"[2] tools/list OK: {[t.name for t in tools.tools]}")
            r1 = await session.call_tool("list_materials", {})
            print(f"[3] list_materials -> {str(r1.content[0].text)[:120]}...")
            r2 = await session.call_tool("get_price_summary",
                                         {"materials": "LUMBER,STEEL,CEMENT,WIRE"})
            data = json.loads(r2.content[0].text)
            print("[4] get_price_summary:")
            for row in data:
                print("    ", json.dumps(row, ensure_ascii=False))
            r3 = await session.call_tool("get_price_history",
                                         {"material": "WPU10170501", "start_date": "2026-01-01"})
            h = json.loads(r3.content[0].text)
            print(f"[5] get_price_history WPU10170501: count={h['count']} last={h['observations'][-1]}")
    print(f"ALL PASSED in {time.time()-t0:.1f}s")
    return 0


sys.exit(asyncio.run(main()))
