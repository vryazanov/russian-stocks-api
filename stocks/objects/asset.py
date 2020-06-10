"""Objects to work with investment portfolio."""
import decimal
import typing

import flask_restx

from stocks.objects.abc import ANY_PRIMITIVE, BaseEntity


class Asset(BaseEntity):
    """Investment asset."""

    def __init__(self, owner: str, ticker: str, quantity: int):
        """Primary constructor."""
        self._owner = owner
        self._ticker = ticker
        self._quantity = quantity

    def price(self, amount: decimal.Decimal) -> decimal.Decimal:
        """Return the price of asset."""
        return self._quantity * amount

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
