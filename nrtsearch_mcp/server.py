"""
Minimal FastMCP server that exposes one tool: nrtsearch/search
──────────────────────────────────────────────────────────────
• Accepts **any** Lucene query the caller provides.
• Normalises bare keywords → text:"…" so phrase tests still work.
• Validates topHits (1-100) to avoid runaway requests.
• Returns   [{"score": …, "stars": …, "text": …}]  – easy for Copilot to display.
"""

import logging
from typing import List, Optional

import httpx
from fastmcp import FastMCP
from pydantic import BaseModel

logger = logging.getLogger(__name__)

mcp = FastMCP("nrtsearch")          # host / port / path supplied at run()

# ────────── result schema ─────────────────────────────────────────────────────
class Hit(BaseModel):
    score: float
    stars: int
    text: str


class SearchResult(BaseModel):
    hits: List[Hit]


# ────────── MCP tool ──────────────────────────────────────────────────────────
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
) -> SearchResult:
    """
    index         – index name (e.g. yelp_reviews_staging)
    queryText     – **Full Lucene query**. If no field or quotes are present the
                    string is treated as a phrase on the `text` field, i.e.
                    → text:"…"
    topHits       – 1-100 results (default 10)
    retrieveFields – optional extra fields; defaults to ["text", "stars"]
    """
    # ── sanity-check inputs ───────────────────────────────────────────────────
    topHits = max(1, min(topHits, 100))
    if "text:" not in queryText and '"' not in queryText:
        queryText = f'text:"{queryText}"'

    retrieveFields = retrieveFields or ["text", "stars"]

    logger.info("→ search %s | %r | top=%s", index, queryText, topHits)

    # ── call the HTTP wrapper ────────────────────────────────────────────────
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(
            "http://localhost:8080/v1/search",
            json={
                "indexName": index,
                "queryText": queryText,
                "topHits": topHits,
                "retrieveFields": retrieveFields,
            },
        )
        resp.raise_for_status()
        raw = resp.json()

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


# ────────── run the server ────────────────────────────────────────────────────

def entrypoint():
    # CLI entry-point for nrtsearch-mcp-server
    main()

def main():
    # Streamable-HTTP endpoint on http://127.0.0.1:3000/
    mcp.run(transport="http", host="127.0.0.1", port=3000, path="/")

if __name__ == "__main__":
    entrypoint()
