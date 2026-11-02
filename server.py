#!/usr/bin/env python3
"""materials-mcp server: 海外建材价格 MCP server (FRED 数据源, 免key).

工具:
  1. list_materials      - 列出支持的建材序列(机器可读目录)
  2. get_price_history   - 拉取单/多序列价格历史(本地CSV缓存优先)
  3. get_price_summary   - 最新值 + 30日均值 + 12个月变动率

数据源: https://fred.stlouisfed.org/graph/fredgraph.csv?id=<SERIES>
可用环境变量 MATERIALS_MCP_BASE_URL 覆盖(应对中国大陆直连FRED失败/被墙场景,
指向任意兼容 fredgraph.csv 格式的镜像)。
缓存: data/cache/<ID>.csv, TTL 24h (FRED PPI 为月度数据, 每日刷新足够)。
"""
from __future__ import annotations

import csv
import io
import json
import os
import re
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from mcp.server.mcpserver import MCPServer

BASE_URL = os.environ.get(
    "MATERIALS_MCP_BASE_URL", "https://fred.stlouisfed.org/graph/fredgraph.csv"
)
CACHE_DIR = Path(__file__).parent / "data" / "cache"
CATALOG_PATH = Path(__file__).parent / "data" / "series_catalog.json"
CACHE_TTL = 24 * 3600  # seconds

mcp = MCPServer(
    "materials-prices",
    instructions="美国建材PPI价格历史(源:BLS via FRED, 月度, 指数值). 用 list_materials 查可用序列.",
)


def _load_catalog() -> list[dict]:
    with open(CATALOG_PATH, encoding="utf-8") as f:
        return json.load(f)["series"]


CATALOG = _load_catalog()
ALIAS = {}
for s in CATALOG:
    ALIAS[s["material"].upper()] = s["fred_id"]
    ALIAS[s["fred_id"].upper()] = s["fred_id"]
# 常用口语别名
ALIAS.update({
    "LUMBER": "WPU1011", "WOOD": "WPU1011", "STUD": "WPU0811",
    "STEEL": "WPU1017", "REBAR": "WPU10170501", "ALUMINUM": "WPU102501",
    "COPPER": "WPUSI019011", "CONCRETE": "PCU327320327320",
    "CEMENT": "WPU132201", "DRYWALL": "PCU327420327420P",
    "WIRE": "PCU335929335929F",
})


def _resolve(name: str) -> str | None:
    return ALIAS.get(name.strip().upper())


def _http_get(url: str) -> str:
    """多级回退取数: 显式代理 -> 直连 -> curl。实测本机环境 urllib 自动代理检测会卡死."""
    import subprocess
    import urllib.request as U

    proxies = {k: v for k, v in {"https": os.environ.get("HTTPS_PROXY", ""),
                                 "http": os.environ.get("HTTP_PROXY", "")}.items() if v}
    attempts = []
    if proxies:
        attempts.append(U.build_opener(U.ProxyHandler(proxies)))
    attempts.append(U.build_opener(U.ProxyHandler({})))  # 直连
    hdrs = {"User-Agent": "materials-mcp/0.1"}
    for opener in attempts:
        try:
            req = U.Request(url, headers=hdrs)
            with opener.open(req, timeout=15) as r:
                if r.status == 200:
                    return r.read().decode("utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            continue
    # 最后回退 curl（某些沙箱/代理栈只放行 curl）
    p = subprocess.run(["curl", "-sS", "--max-time", "20", url],
                       capture_output=True, text=True)
    if p.returncode == 0 and p.stdout.strip():
        return p.stdout
    raise RuntimeError(f"所有取数方式均失败 (proxy/direct/curl): {p.stderr[:200] if p.stderr else ''}")


def _fetch_csv(series_id: str) -> str:
    """返回CSV文本; 本地缓存命中则不发请求."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache = CACHE_DIR / f"{series_id}.csv"
    if cache.exists() and time.time() - cache.stat().st_mtime < CACHE_TTL:
        return cache.read_text(encoding="utf-8")
    url = f"{BASE_URL}?id={series_id}&obs_start=2015-01-01"
    text = _http_get(url)
    cache.write_text(text, encoding="utf-8")
    return text


def _parse_csv(text: str, series_id: str) -> list[tuple[str, float]]:
    rows: list[tuple[str, float]] = []
    rdr = csv.reader(io.StringIO(text))
    header = next(rdr, None)
    if not header:
        return rows
    for row in rdr:
        if len(row) < 2 or not row[0] or row[1] in ("", ".", ""):
            continue
        try:
            rows.append((row[0], float(row[1])))
        except ValueError:
            continue
    return rows


@mcp.tool()
def list_materials() -> str:
    """列出所有支持的建材及其FRED序列ID(含中文), 返回JSON."""
    out = [
        {"material": s["material"], "cn": s.get("cn", ""), "fred_id": s["fred_id"],
         "title": s.get("title", ""), "last_obs": s.get("last_obs"),
         "status": "DEAD" if s.get("http") == 404 else ("STALE" if (s.get("last_obs") or "") < "2025" else "OK")}
        for s in CATALOG
    ]
    return json.dumps(out, ensure_ascii=False, indent=2)


@mcp.tool()
def get_price_history(material: str, start_date: str = "2024-01-01",
                      end_date: str = "") -> str:
    """获取某建材价格指数的历史序列. material 可为FRED ID或别名(LUMBER/STEEL/REBAR/CEMENT...).

    返回JSON: {series_id, title, unit, observations:[{date,value}]}
    """
    sid = _resolve(material)
    if not sid:
        return json.dumps({"error": f"unknown material '{material}', call list_materials"})
    meta = next((s for s in CATALOG if s["fred_id"] == sid), {})
    if meta.get("http") == 404:
        return json.dumps({"error": f"{sid} 序列已失效(404)", "material": sid})
    try:
        text = _fetch_csv(sid)
    except Exception as e:  # noqa: BLE001
        return json.dumps({"error": f"fetch failed: {e}", "hint": "可设置 MATERIALS_MCP_BASE_URL 指向镜像"})
    obs = _parse_csv(text, sid)
    obs = [(d, v) for d, v in obs if d >= start_date and (not end_date or d <= end_date)]
    return json.dumps({
        "series_id": sid, "title": meta.get("title", ""),
        "unit": "PPI Index (见title), 月度", "count": len(obs),
        "observations": [{"date": d, "value": v} for d, v in obs],
    }, ensure_ascii=False)


@mcp.tool()
def get_price_summary(materials: str) -> str:
    """一次获取多个建材的最新指数/12个月变动率. materials=逗号分隔(如 LUMBER,STEEL,CEMENT).

    返回JSON数组, 每项: {material, cn, fred_id, latest_date, latest_value, mom_pct, yoy_pct}
    """
    results = []
    for name in [m.strip() for m in materials.split(",") if m.strip()]:
        sid = _resolve(name)
        if not sid:
            results.append({"input": name, "error": "unknown material"})
            continue
        meta = next((s for s in CATALOG if s["fred_id"] == sid), {})
        try:
            obs = _parse_csv(_fetch_csv(sid), sid)
        except Exception as e:  # noqa: BLE001
            results.append({"material": name, "fred_id": sid, "error": str(e)})
            continue
        if len(obs) < 2:
            results.append({"material": name, "fred_id": sid, "error": "insufficient data"})
            continue
        latest_d, latest_v = obs[-1]
        prev_v = obs[-2][1]
        idx = len(obs) - 13
        yoy_v = obs[idx][1] if idx >= 0 else None
        results.append({
            "material": meta.get("material", name), "cn": meta.get("cn", ""),
            "fred_id": sid, "latest_date": latest_d, "latest_value": latest_v,
            "mom_pct": round((latest_v / prev_v - 1) * 100, 2),
            "yoy_pct": round((latest_v / yoy_v - 1) * 100, 2) if yoy_v else None,
        })
    return json.dumps(results, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")
