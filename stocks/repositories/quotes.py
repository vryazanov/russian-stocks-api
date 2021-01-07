"""Repositories for quotes."""
import sqlalchemy.orm

from stocks import db
from stocks.entities import QuoteBase
from stocks.repositories.abc import BaseRepository


class Quotes(BaseRepository[QuoteBase]):
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

    def add(self, entity: QuoteBase):
        """Save ticker to db."""
        self._session.add(
            db.QuoteModel(
                ticker=entity.ticker,
                date=entity.date,
                open_price=entity.open_price,
                close_price=entity.close_price,
            ),
        )
