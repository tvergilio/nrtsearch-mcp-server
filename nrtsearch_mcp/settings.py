from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    gateway_url: str = "http://localhost:8080"
    host: str = "127.0.0.1"
    port: int = 3000
    total_timeout: float = 10.0
    per_attempt_timeout: float = 5.0
    log_level: str = "INFO"
    # Per-index and global retrieveFields defaults
    default_retrieve_fields: dict = {
        "yelp_reviews_staging": ["text", "stars"],
        # Add more index-specific defaults as needed
    }
    default_retrieve_fields_global: list = ["text"]  # fallback if index-specific not found

    model_config = SettingsConfigDict(env_prefix="NMCP_", env_file=".env")
