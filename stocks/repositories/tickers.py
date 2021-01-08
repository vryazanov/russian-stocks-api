"""Repositories for tickers."""
import typing

import sqlalchemy.orm
import typing_extensions

from stocks import db
from stocks.entities import Ticker
from stocks.repositories.abc import BaseRepository


class TickerFilters(typing_extensions.TypedDict):
    """Possible filters for tickers."""


class Tickers(
    BaseRepository[
        Ticker,
        Ticker,
        Ticker,
        TickerFilters,
    ],
):
    """Tickers repository."""

    def __init__(self, session: sqlalchemy.orm.Session):
        """Primary constructor."""
        self._session = session

    def exists(self, entity: Ticker) -> bool:
        """Return true if ticker exists."""
        return bool(self._session.query(db.TickerModel).get(entity.code))

    def add(self, entity: Ticker) -> None:
        """Save ticker to db."""
        self._session.add(
            db.TickerModel(
                name=entity.name,
                code=entity.code,
                lot=entity.lot,
            ),
        )

    def iterator(self, filters: TickerFilters) -> typing.List[Ticker]:
        """Return list of tickers."""
        query = self._session.query(db.TickerModel).all()
        return [Ticker.from_orm(ticker) for ticker in query]
