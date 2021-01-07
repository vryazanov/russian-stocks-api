"""Repositories for tickers."""
import sqlalchemy.orm

from stocks import db
from stocks.entities import Ticker
from stocks.repositories.abc import BaseRepository


class Tickers(BaseRepository[Ticker]):
    """Tickers repository."""

    def __init__(self, session: sqlalchemy.orm.Session):
        """Primary constructor."""
        self._session = session

    def exists(self, entity: Ticker) -> bool:
        """Return true if ticker exists."""
        return bool(self._session.query(db.TickerModel).get(entity.code))

    def add(self, entity: Ticker):
        """Save ticker to db."""
        self._session.add(
            db.TickerModel(
                name=entity.name,
                code=entity.code,
            ),
        )
