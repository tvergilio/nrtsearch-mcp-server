"""
Minimal FastMCP server that exposes one tool: nrtsearch/search
──────────────────────────────────────────────────────────────
• Accepts **any** Lucene query the caller provides.
• Normalises bare keywords → text:"…" so phrase tests still work.
• Validates topHits (1-100) to avoid runaway requests.
• Returns   [{"score": …, "stars": …, "text": …}]  – easy for Copilot to display.
"""


import logging
import os
from typing import List, Optional
import httpx
import asyncio
from fastmcp import FastMCP
from pydantic import BaseModel
from nrtsearch_mcp.settings import Settings


# Structured logging setup
logger = logging.getLogger("nrtsearch.mcp")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logger.setLevel(getattr(logging, log_level, logging.INFO))

settings = Settings()
mcp = FastMCP("nrtsearch")          # host / port / path supplied at run()

# ────────── result schema ─────────────────────────────────────────────────────
class Hit(BaseModel):
    score: float
    stars: int
    text: str


class SearchResult(BaseModel):
    hits: List[Hit]


# ────────── MCP tool ──────────────────────────────────────────────────────────

# Private implementation for search logic, for direct unit testing
async def _search_impl(
    index: str,
    queryText: str,
    topHits: int = 10,
    retrieveFields: Optional[List[str]] = None,
    highlight: bool = False,
) -> SearchResult:
    """
    Core search logic for NRTSearch/Lucene index. Used by the tool and for direct unit testing.
    """
    # ── sanity-check inputs ───────────────────────────────────────────────────
    topHits = max(1, min(topHits, 100))
    if "text:" not in queryText and '"' not in queryText:
        queryText = f'text:"{queryText}"'

    retrieveFields = retrieveFields or ["text", "stars"]

    logger.info("→ search %s | %r | top=%s", index, queryText, topHits)

    # ── call the HTTP wrapper ────────────────────────────────────────────────
    attempt = 0
    max_attempts = 3
    backoff = 0.1
    while True:
        try:
            async with httpx.AsyncClient(timeout=settings.timeout) as client:
                payload = {
                    "indexName": index,
                    "queryText": queryText,
                    "topHits": topHits,
                    "retrieveFields": retrieveFields,
                }
                if highlight:
                    payload["highlightFields"] = ["text"]
                resp = await client.post(
                    f"{settings.gateway_url}/v1/search",
                    json=payload,
                )
                resp.raise_for_status()
                raw = resp.json()
            break
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            attempt += 1
            logger.warning(f"Gateway call failed (attempt {attempt}): {e}")
            if attempt >= max_attempts:
                logger.error("Max retry attempts reached. Raising error.")
                raise
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 0.8)

    # ── reshape results for Copilot ──────────────────────────────────────────
    hits: List[Hit] = []
    for hit in raw.get("hits", []):
        fields = hit["fields"]
        hits.append(
            Hit(
                score=hit["score"],
                stars=fields["stars"]["fieldValue"][0]["intValue"],
                text=fields["text"]["fieldValue"][0]["textValue"],
            )
        )

    return SearchResult(hits=hits)


# MCP tool wrapper calls the private implementation
@mcp.tool(
    description="Search an NRTSearch/Lucene index",
    annotations={
        "parameters": {
            "properties": {
                "queryText": {
                    "description": (
                        "Lucene Boolean query **required**.\n"
                        "• Join keywords with AND/OR/NOT  → text:(gay AND bar AND sf)\n"
                        "• Use quotes for phrases         → text:\"great coffee\"\n"
                        "• Range / wildcard / fuzzy ok    → stars:[4 TO 5], bar*, cocktail~1"
                    )
                }
            }
        },
        "examples": [
            {  # Boolean keywords
                "index": "yelp_reviews_staging",
                "queryText": 'text:(irish AND pub AND (texas OR tx))',
                "topHits": 3
            },
            {  # Phrase
                "index": "yelp_reviews_staging",
                "queryText": 'text:"great coffee"',
                "topHits": 5
            }
        ],
    },
)
async def search(
    index: str,
    queryText: str,
    topHits: int = 10,
    retrieveFields: Optional[List[str]] = None,
    highlight: bool = False,
) -> SearchResult:
    return await _search_impl(index, queryText, topHits, retrieveFields, highlight)


# ────────── run the server ────────────────────────────────────────────────────

def entrypoint():
    # CLI entry-point for nrtsearch-mcp-server
    main()


def main():
    # Streamable-HTTP endpoint on http://host:port/
    mcp.run(transport="http", host=settings.host, port=settings.port, path="/")

if __name__ == "__main__":
    entrypoint()
