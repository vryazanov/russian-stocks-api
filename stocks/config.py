"""Application config."""
import os


class Config:
    """Main application config.

    It takes settings from environment variables.
    """

    MONGODB_URI = os.environ['MONGODB_URI']
    AUTH_IMPORT_TOKEN = os.environ['AUTH_IMPORT_TOKEN']
