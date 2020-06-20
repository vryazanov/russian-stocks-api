"""Objects to work with investment portfolio."""
import datetime
import decimal
import typing

import flask_restx

from stocks.filters.query import PaymentQuery
from stocks.objects.abc import ANY_PRIMITIVE, BaseEntity


if typing.TYPE_CHECKING:
    from stocks.repostories import Payments


class Asset(BaseEntity):
    """Investment asset."""

    def __init__(
        self, owner: str, ticker: str, quantity: int, payments: 'Payments',
    ):
        """Primary constructor."""
        self._owner = owner
        self._ticker = ticker
        self._quantity = quantity
        self._payments = payments

    def price(self, amount: decimal.Decimal) -> decimal.Decimal:
        """Return the price of asset."""
        return self._quantity * amount

    def dividends_within_date_range(
        self, date_from: datetime.date, date_to: datetime.date,
    ) -> decimal.Decimal:
        """Calculate amount of dividends within date range."""
        payments = self._payments.search(
            PaymentQuery().within_date_range(self._ticker, date_from, date_to))
        return decimal.Decimal(
            sum(payment.amount() * self._quantity for payment in payments))

    @classmethod
    def as_model(cls) -> flask_restx.Model:
        """Swagger model from class."""
        return flask_restx.Model('Asset', {
            'ticker': flask_restx.fields.String(
                required=True,
                description='code of ticker',
                example='SBER',
            ),
            'quantity': flask_restx.fields.Integer(
                required=True,
                description='number of stocks',
                example=10,
            ),
        })

    def as_dict(self) -> typing.Dict[str, ANY_PRIMITIVE]:
        """Serialize asset."""
        return {
            'ticker': self._ticker,
            'quantity': self._quantity,
            'owner': self._owner,
        }


AssetModel = Asset.as_model()
