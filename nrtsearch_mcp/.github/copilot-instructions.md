# Project instructions for GitHub Copilot

* The MCP server `nrtsearch/search` **only accepts Lucene syntax**  
  (Boolean operators, quoted phrases, ranges, wildcards, fuzzies).  
  Always build a Lucene query before calling the tool.

Examples  
• text:(irish AND pub AND (texas OR tx))  
• text:"great coffee"  
• stars:[4 TO 5] AND text:(vegan AND brunch)
