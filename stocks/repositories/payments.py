"""Repositories for tickers."""
import typing

import sqlalchemy.orm
import typing_extensions

from stocks import db
from stocks.entities import PaymentBase, Payment, PaymentCreate
from stocks.repositories.abc import BaseRepository


class PaymentFilters(typing_extensions.TypedDict):
    """Possible filters for payments."""

    ticker: str


class Payments(
    BaseRepository[
        Payment,
        PaymentBase,
        PaymentCreate,
        PaymentFilters,
    ],
):
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

    def add(self, entity: PaymentCreate) -> None:
        """Save ticker to db."""
        self._session.add(
            db.PaymentModel(
                ticker=entity.ticker,
                date=entity.date,
                amount=float(entity.amount),
                is_forecast=entity.is_forecast,
                source=entity.source,
            ),
        )

    def iterator(self, filters: PaymentFilters) -> typing.List[Payment]:
        """Return list of payments."""
        query = self._session.query(db.PaymentModel).filter(
            db.PaymentModel.ticker == filters['ticker'],
        )
        return [Payment.from_orm(payment) for payment in query]
