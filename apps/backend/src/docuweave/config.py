from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Template DB
    template_db_type: str = "postgres"  # postgres | mysql | mongodb
    template_db_url: str = "postgresql+asyncpg://docuweave:docuweave@localhost:5432/docuweave_templates"

    # Data DB
    data_db_type: str = "postgres"  # postgres | mysql | mongodb
    data_db_url: str = "postgresql://docuweave:docuweave@localhost:5433/docuweave_data"

    # Server
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    debug: bool = False


settings = Settings()
