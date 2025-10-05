from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    app_name: str = "Job Opening WhatsApp Bot"
    debug: bool = False
    
    # PostgreSQL
    database_url: str = "postgresql://postgres:postgres@localhost:5432/job_opening_bot"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "job_opening_bot"
    db_user: str = "postgres"
    db_password: str = "postgres"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    
    # Session configuration
    session_timeout_minutes: int = 30
    message_timeout_minutes: int = 5
    
    # WhatsApp API (WAHA)
    waha_api_url: str = "http://localhost:3000"
    waha_api_token: str = ""
    
    # OpenAI / ChatGPT
    openai_api_key: str = ""
    openai_model: str = "gpt-4"
    
    # Rate limiting
    rate_limit_messages_per_minute: int = 10
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


settings = Settings()

