from pydantic_settings import SettingsConfigDict, BaseSettings
from dotenv import load_dotenv

load_dotenv()


class AppSettings(BaseSettings):
    # DB
    db_create: bool = False
    db_host: str | None = "localhost"
    db_port: str | None = "5432"
    db_user: str | None = "user"
    db_password: str | None = "password"
    db_name: str | None = "notifications_db"
    db_debug: bool = False
    db_pool_size: int = 20
    db_max_overflow: int = 10

    # Redis
    redis_host: str = "localhost"
    redis_port: str = "6379"
    redis_password: str = ""
    redis_user: str = ""
    redis_db: int = 2
    redis_max_pool_connections: int = 5

    # API
    api_host: str | None = "0.0.0.0"
    api_port: int | None = 8000
    api_title: str | None = "Notifications API"
    api_root_path: str | None = "/api"

    # SEC
    sec_public_secret_key: bytes = "public_secret_key"
    sec_algorithm: str = "RS256"

    # Kafka
    kafka_user: str | None = None
    kafka_password: str | None = None
    kafka_servers: list[str] = ["localhost:29093"]
    kafka_topic_users: str = "users"

    # COMMON
    debug: bool = False
    model_config = SettingsConfigDict(env_ignore_empty=True, extra="ignore", env_prefix="NOTIFICATIONS_")


settings = AppSettings()
