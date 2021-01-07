"""Application settings."""
import os

import pydantic


class Settings(pydantic.BaseSettings):
    """Main application config.

    It takes settings from environment variables.
    """

    sqlalchemy_uri: str = os.environ['SQLALCHEMY_URI']
    import_token: str = os.environ['AUTH_IMPORT_TOKEN']
