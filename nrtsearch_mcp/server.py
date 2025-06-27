from fastmcp import FastMCP
import httpx

mcp = FastMCP("nrtsearch")          # ◀─ no host/port/path here

@mcp.tool(description="Search an NRTSearch/Lucene index")
async def search(index: str, query: str, topHits: int = 10) -> dict:
    """
    index   – index name
    query   – Lucene query
    topHits – results to return (default 10)
    """
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(
            "http://localhost:8080/v1/search",
            json={
                "indexName": index,
                "queryText": query,
                "topHits": topHits,
                "retrieveFields": ["text", "stars"]
            },
        )
        r.raise_for_status()
        return r.json()

if __name__ == "__main__":
    # Exposes Streamable-HTTP MCP on http://127.0.0.1:3000/
    mcp.run(transport="http", host="127.0.0.1", port=3000, path="/")
