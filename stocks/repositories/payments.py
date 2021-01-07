"""Repositories for tickers."""
import sqlalchemy.orm

from stocks import db
from stocks.entities import PaymentBase
from stocks.repositories.abc import BaseRepository


class Payments(BaseRepository[PaymentBase]):
    """Tickers repository."""

    def __init__(self, session: sqlalchemy.orm.Session):
        """Primary constructor."""
        self._session = session

    def exists(self, entity: PaymentBase) -> bool:
        """Return true if ticker exists."""
        return bool(
            self._session.query(db.PaymentModel).filter(
                db.PaymentModel.date == entity.date,
                db.PaymentModel.ticker == entity.ticker,
            ).first(),
        )

    def add(self, entity: PaymentBase):
        """Save ticker to db."""
        self._session.add(
            db.PaymentModel(
                ticker=entity.ticker,
                date=entity.date,
                amount=entity.amount,
                is_forecast=entity.is_forecast,
                source=entity.source,
            ),
        )
