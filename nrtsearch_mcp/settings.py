from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    gateway_url: str = "http://localhost:8080"
    host: str = "127.0.0.1"
    port: int = 3000
    timeout: float = 10.0
    total_timeout: float = 10.0
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_prefix="NMCP_", env_file=".env")
