"""Repositories for quotes."""
import datetime
import typing

import sqlalchemy.orm
import typing_extensions

from stocks import db
from stocks.entities import Quote, QuoteBase, QuoteCreate
from stocks.repositories.abc import BaseRepository


class QuoteFilters(typing_extensions.TypedDict):
    """Possible filters for quotes."""

    ticker: str
    date: datetime.date


class Quotes(
    BaseRepository[
        Quote,
        QuoteBase,
        QuoteCreate,
        QuoteFilters,
    ],
):
    """Tickers repository."""

    def __init__(self, session: sqlalchemy.orm.Session):
        """Primary constructor."""
        self._session = session

    def exists(self, entity: QuoteBase) -> bool:
        """Return true if ticker exists."""
        return bool(
            self._session.query(db.QuoteModel).filter(
                db.QuoteModel.date == entity.date,
                db.QuoteModel.ticker == entity.ticker,
            ).first(),
        )

    def add(self, entity: QuoteCreate) -> None:
        """Save ticker to db."""
        self._session.add(
            db.QuoteModel(
                ticker=entity.ticker,
                date=entity.date,
                open_price=float(entity.open_price),
                close_price=float(entity.close_price),
            ),
        )

    def iterator(self, filters: QuoteFilters) -> typing.List[Quote]:
        """Return list of quotes."""
        query = self._session.query(db.QuoteModel).filter(
            db.QuoteModel.ticker == filters['ticker'],
            db.QuoteModel.date == filters['date'],
        )
        return [Quote.from_orm(quote) for quote in query]
