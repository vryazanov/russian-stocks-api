"""A set of dependencies used by Fast APi."""
import fastapi
import sqlalchemy
import sqlalchemy.orm

from stocks.repositories.uow import UoW
from stocks.settings import Settings


def get_settings() -> Settings:
    """Build an instance of settings."""
    return Settings()


def get_uow(settings: Settings = fastapi.Depends(get_settings)) -> UoW:
    """Build an instance of unit of work."""
    session_factory = sqlalchemy.orm.sessionmaker(
        autocommit=False, autoflush=False,
        bind=sqlalchemy.create_engine(settings.sqlalchemy_uri))
    return UoW(session_factory)
