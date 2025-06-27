## How to write queries for the NRTSearch tool

- Always use explicit Lucene syntax in the `queryText` parameter.
- For best results, specify the field, e.g. `text:(port AND brandy)` instead of just `port brandy`.

- Example for searching both “port” and “brandy” in the same document:

    ```json
    {
      "index": "yelp_reviews_staging",
      "queryText": "text:(port AND brandy)",
      "topHits": 3
    }
    ```

- To search for synonyms or alternatives (e.g., reviews mentioning either "San Francisco" or "SF"), use:

    ```json
    {
      "index": "yelp_reviews_staging",
      "queryText": "text:(\"San Francisco\" OR SF)",
      "topHits": 3
    }
    ```

- To search for an exact phrase (e.g., "sweet potato"), use:

    ```json
    {
      "index": "yelp_reviews_staging",
      "queryText": "text:\"sweet potato\"",
      "topHits": 3
    }
    ```

- To combine a keyword and a phrase (e.g., reviews mentioning both 'lovely' and the phrase "sweet potato"), use:

    ```json
    {
      "index": "yelp_reviews_staging",
      "queryText": "text:(lovely AND \"sweet potato\")",
      "topHits": 3
    }
    ```      
  
- See the tool’s annotation for more Lucene examples:
  - Boolean: `text:(irish AND pub AND (texas OR tx))`
  - Phrase: `text:"great coffee"`
  - Range: `stars:[4 TO 5]`
  - Wildcard: `bar*`
  - Fuzzy: `cocktail~1`

# Project instructions for GitHub Copilot

* The MCP server `nrtsearch/search` **only accepts Lucene syntax**  
  (Boolean operators, quoted phrases, ranges, wildcards, fuzzies).  
  Always build a Lucene query before calling the tool.

Examples  
• text:(irish AND pub AND (texas OR tx))  
• text:"great coffee"  
• stars:[4 TO 5] AND text:(vegan AND brunch)
