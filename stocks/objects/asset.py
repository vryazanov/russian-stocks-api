"""Objects to work with investment portfolio."""
import decimal

import flask_restx

from stocks.objects.abc import BaseEntity


class Asset(BaseEntity):
    """Investment asset."""

    def __init__(self, ticker: str, quantity: int):
        """Primary constructor."""
        self._ticker = ticker
        self._quantity = quantity

    def price(self, amount: decimal.Decimal) -> decimal.Decimal:
        """Return the price of asset."""
        return self._quantity * amount

    @classmethod
    def as_model(cls):
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

    def as_dict(self):
        """Serialize asset."""
        return {
            'ticker': self._ticker,
            'quantity': self._quantity,
        }
