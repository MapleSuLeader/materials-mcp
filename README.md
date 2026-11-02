# materials-mcp

**US construction material prices for AI agents — free, 33 FRED series via MCP.**

An MCP (Model Context Protocol) server that gives Claude Code, Cursor, and any other
MCP client direct access to US construction-material price indices (PPI), sourced from
**FRED (BLS data)** with **no API key required**. Runs locally over stdio.

## Why

Steel mill products are up **+27.6% year-over-year** (WPU1017, Sep 2026) while the
average material in RSMeans' 2026 annual report moved only **+3.9%** — metal categories
are the blind spot in small-contractor estimates. This server lets your agent pull the
official long-run index for lumber, rebar, cement, wire, drywall, aluminum, copper and
27 more series in one tool call, so quotes track reality instead of last year's catalog.

## Quick start

```bash
# Python 3.12+, uv recommended (any venv works)
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python "mcp>=2.0"

# End-to-end self test: stdio handshake -> tools/list -> 3 live tool calls
.venv/bin/python test_client.py
```

Wire into Claude Code (project `.mcp.json`) or Cursor (`~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "materials-prices": {
      "command": "/absolute/path/to/.venv/bin/python",
      "args": ["/absolute/path/to/server.py"]
    }
  }
}
```

## Demo (real terminal output, 2026-11-02)

```text
[1] handshake OK: server=materials-prices protocol=2025-11-25
[2] tools/list OK: ['list_materials', 'get_price_history', 'get_price_summary']
[3] list_materials -> [
  {
    "material": "lumber",
    "cn": "木材/成材",
    "fred_id": "WPU1011",
    "title": "PPI Commodity: Lumber and Woo...
[4] get_price_summary:
     {"material": "lumber", "cn": "木材/成材", "fred_id": "WPU1011", "latest_date": "2026-09-01", "latest_value": 206.602, "mom_pct": 0.0, "yoy_pct": 0.38}
     {"material": "steel_mill", "cn": "钢铁厂产品", "fred_id": "WPU1017", "latest_date": "2026-09-01", "latest_value": 388.58, "mom_pct": 2.16, "yoy_pct": 27.58}
     {"material": "portland_cement", "cn": "波特兰水泥", "fred_id": "WPU132201", "latest_date": "2026-09-01", "latest_value": 356.209, "mom_pct": 0.03, "yoy_pct": -1.18}
     {"material": "insulated_wire", "cn": "绝缘电线电缆", "fred_id": "PCU335929335929F", "latest_date": "2026-09-01", "latest_value": 193.549, "mom_pct": -6.74, "yoy_pct": 14.2}
[5] get_price_history WPU10170501: count=9 last={'date': '2026-09-01', 'value': 362.132}
ALL PASSED in 88.5s
```

Full log: [`docs/demo-output.txt`](docs/demo-output.txt). Latest observations are
2026-09-01 — that is the freshest published BLS monthly print as of 2026-11-02
(October PPI typically releases ~Nov 20). Values are PPI index numbers (base-period
indexed, e.g. 1982=100), not absolute dollar prices.

## Tools

| Tool | Description |
|---|---|
| `list_materials()` | Machine-readable catalog of 33 verified FRED series (id, title, latest observation, OK/STALE/DEAD status) |
| `get_price_history(material, start_date, end_date)` | Full monthly history for one series. Accepts FRED ids or aliases: `LUMBER`, `STEEL`, `REBAR`, `CEMENT`, `WIRE`, `COPPER`, `ALUMINUM`, `CONCRETE`, `DRYWALL`… |
| `get_price_summary(materials)` | Batch call: latest value + MoM% + YoY% for a comma-separated list (e.g. `LUMBER,STEEL,CEMENT`) |

## Data & networking

- Source: `https://fred.stlouisfed.org/graph/fredgraph.csv?id=<SERIES>` — public, keyless.
- Fetch fallback chain: explicit proxy → direct → curl. Cache: `data/cache/<ID>.csv`, 24h TTL.
  Cold run ≈ 80s, cached run ≈ 1s.
- Mainland-China note: direct FRED access can be unreliable there. Set
  `MATERIALS_MCP_BASE_URL` to any fredgraph-compatible mirror, or use the hosted endpoint.
- Series validation evidence lives in `data/series_catalog.json` (per-series HTTP status +
  last observation). Dead/discontinued series (WPU101201, WPU1324, WPU107703 … 404;
  WPU101703, WPU1077 stale since 2022) are marked and rejected gracefully.

## Pricing

The open-source stdio server is free forever (MIT). A hosted **PRO tier**
(streamable-HTTP endpoint, daily refresh, multi-series diffs, alerting) is planned at
$19/mo — see `docs/proposal-pricing-acquisition.md` for the full positioning; no
sign-up link is live yet.

## License

MIT — see [LICENSE](LICENSE). BLS/FRED data is public; attribution requested.
