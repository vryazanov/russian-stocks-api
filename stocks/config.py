"""Application config."""
import os


class Config:
    """Main application config.

    It takes settings from environment variables.
    """

    MONGODB_URI = os.environ['MONGODB_URI']
