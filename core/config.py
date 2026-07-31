#core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str = 'development'
    secret_key: str
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 60
    database_url: str
    redis_url: str
    ollama_base_url: str = 'http://localhost:11434'
    gemini_api_key: str = ''
    gcp_project_id: str = ''
    class Config:
        env_file = '.env'
 
settings = Settings()

