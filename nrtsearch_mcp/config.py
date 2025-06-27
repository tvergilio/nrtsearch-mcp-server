"""
Configuration handling for the NRTSearch MCP server.
"""

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class NRTSearchConnection:
    """NRTSearch server connection configuration."""
    
    host: str
    port: int
    use_https: bool = False
    
    @property
    def url(self) -> str:
        """Get the URL for the NRTSearch server."""
        protocol = "https" if self.use_https else "http"
        return f"{protocol}://{self.host}:{self.port}"


@dataclass
class IndexConfig:
    """Configuration for a specific NRTSearch index."""
    
    name: str
    description: str
    fields: List[str]
    default_search_fields: List[str]


@dataclass
class ServerConfig:
    """Main configuration for the NRTSearch MCP server."""
    
    nrtsearch_connection: NRTSearchConnection
    indexes: List[IndexConfig]
    log_level: str = "INFO"


def load_config(config_path: Optional[str] = None) -> ServerConfig:
    """
    Load the server configuration from a JSON file.
    
    If no config_path is provided, it looks for:
    1. Path in NRTSEARCH_MCP_CONFIG env variable
    2. ./config.json
    3. ~/nrtsearch-mcp-config.json
    """
    if not config_path:
        config_path = os.environ.get("NRTSEARCH_MCP_CONFIG")
        
    if not config_path:
        local_config = Path("./config.json")
        if local_config.exists():
            config_path = str(local_config)
            
    if not config_path:
        home_config = Path.home() / "nrtsearch-mcp-config.json"
        if home_config.exists():
            config_path = str(home_config)
            
    if not config_path or not Path(config_path).exists():
        raise FileNotFoundError(
            "Configuration file not found. Please provide a valid config path."
        )
        
    with open(config_path) as f:
        config_data = json.load(f)
        
    # Parse NRTSearch connection
    connection_data = config_data.get("nrtsearch_connection", {})
    connection = NRTSearchConnection(
        host=connection_data.get("host", "localhost"),
        port=connection_data.get("port", 8000),
        use_https=connection_data.get("use_https", False)
    )
    
    # Parse index configurations
    indexes = []
    for idx_data in config_data.get("indexes", []):
        index = IndexConfig(
            name=idx_data.get("name", ""),
            description=idx_data.get("description", ""),
            fields=idx_data.get("fields", []),
            default_search_fields=idx_data.get("default_search_fields", [])
        )
        indexes.append(index)
    
    # Create the server config
    return ServerConfig(
        nrtsearch_connection=connection,
        indexes=indexes,
        log_level=config_data.get("log_level", "INFO")
    )


def get_default_config() -> ServerConfig:
    """Generate a default configuration for testing or demo purposes."""
    return ServerConfig(
        nrtsearch_connection=NRTSearchConnection(
            host="localhost",
            port=8000
        ),
        indexes=[
            IndexConfig(
                name="yelp_reviews",
                description="Yelp reviews dataset",
                fields=["review_id", "business_id", "stars", "text"],
                default_search_fields=["text"]
            )
        ]
    )
