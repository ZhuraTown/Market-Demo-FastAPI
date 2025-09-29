from pydantic_settings import SettingsConfigDict, BaseSettings
from dotenv import load_dotenv

load_dotenv()

class ApiSettings(BaseSettings):
    host: str | None = "0.0.0.0"
    port: int | None = 8000
    title: str | None = "Users API"
    root_path: str | None = "/api"

    model_config = SettingsConfigDict(env_ignore_empty=True, extra='ignore')

class DBSettings(BaseSettings):
    create: bool = False
    host: str | None = "localhost"
    port: str | None = "5432"
    user: str | None = "user"
    password: str | None = 'password'
    name: str | None = "users_db"
    debug: bool = False
    pool_size: int = 20
    max_overflow: int = 10

    model_config = SettingsConfigDict(env_ignore_empty=True, extra='ignore')

class AppSettings(BaseSettings):

    api: ApiSettings = ApiSettings(env_prefix="USERS_API_") # noqa
    db: DBSettings = DBSettings(env_prefix="USERS_PG_") # noqa


settings = AppSettings()