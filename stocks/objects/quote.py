"""Objects to work with stock quotes."""
import datetime
import decimal
import typing

import flask_restx
import flask_restx.fields

from stocks.objects.abc import ANY_PRIMITIVE, BaseEntity


class Quote(BaseEntity):
    """Stock quote."""

    def __init__(
        self, ticker: str, date: datetime.date, open_price: decimal.Decimal,
        close_price: decimal.Decimal,
    ):
        """Primary constructor."""
        self._ticker = ticker
        self._date = date
        self._open_price = open_price
        self._close_price = close_price

    @classmethod
    def as_model(cls) -> flask_restx.Model:
        """Build swagger model."""
        return flask_restx.Model('HistoricalQuote', {
            'ticker': flask_restx.fields.String(
                required=True,
                description='code of ticker',
                example='SBER',
            ),
            'date': flask_restx.fields.String(
                required=True,
                description='date of stock quote',
                example='2020-04-01',
            ),
            'open_price': flask_restx.fields.Fixed(
                required=True,
            ),
            'close_price': flask_restx.fields.Fixed(
                required=True,
            ),
        })

    def as_dict(self) -> typing.Dict[str, ANY_PRIMITIVE]:
        """Serialize quote."""
        return {
            'ticker': self._ticker,
            'date': self._date.strftime('%Y-%m-%d'),
            'open_price': str(self._open_price),
            'close_price': str(self._close_price),
        }


QuoteModel = Quote.as_model()
