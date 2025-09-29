from passlib.context import CryptContext
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
    db_name: str | None = "users_db"
    db_debug: bool = False
    db_pool_size: int = 20
    db_max_overflow: int = 10

    # API
    api_host: str | None = "0.0.0.0"
    api_port: int | None = 8000
    api_title: str | None = "Users API"
    api_root_path: str | None = "/api"

    # SEC
    sec_public_secret_key: bytes = "public_secret_key"
    sec_private_secret_key: bytes = "private_secret_key"
    sec_ttl_access_token: int = 60 * 60 * 24
    sec_ttl_refresh_token: int = 60 * 60 * 24 * 30
    sec_algorithm: str = "RS256"

    # COMMON
    debug: bool = False
    model_config = SettingsConfigDict(env_ignore_empty=True, extra="ignore", env_prefix="USERS_")


settings = AppSettings()
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto",)