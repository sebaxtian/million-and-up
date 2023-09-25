from os import path
from pathlib import Path

from pydantic_settings import BaseSettings

# Constants
MISSING_SECRET = ">>> missing SECRETS file <<<"
""" Error message for missing secrets file """

MISSING_ENV = ">>> missing ENV value <<<"
""" Error message for missing values in the .env file """


class Settings(BaseSettings):
    """Settings Parameters"""

    # project
    name: str = MISSING_ENV
    version: str = MISSING_ENV
    build_env: str = MISSING_ENV

    # mongodb connection string
    mongodb_url: str = MISSING_SECRET

    # to create JWTs
    # to get a string run: openssl rand -hex 32
    jwt_secret_key: str = MISSING_SECRET
    # HS256
    jwt_algorithm: str = MISSING_SECRET
    # access token expire time
    access_token_expire_minutes: int = MISSING_ENV

    # pytest mode
    pytest_mode: bool = False

    # Handles both local and Docker environments.
    class Config:
        secrets_dir = (
            "/run/secrets"
            if path.exists("/.dockerenv") & path.exists("/run/secrets")
            else f"{Path(__file__).parents[2]}/secrets"
        )
        env_file = f"{Path(__file__).parents[2]}/.env"


settings = Settings()
""" Settings Parameters Instance """
