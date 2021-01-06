"""Application settings."""
import functools
import os

import pydantic


class Settings(pydantic.BaseSettings):
    """Main application config.

    It takes settings from environment variables.
    """

    mongodb_uri: str = os.environ['MONGODB_URI']
    import_token: str = 'some-token'


@functools.lru_cache()
def get_settings() -> Settings:
    """Build an instance of settings."""
    return Settings()
