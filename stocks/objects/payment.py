"""Objects to work with dividend payments."""
import datetime
import decimal

import flask_restx
import flask_restx.fields

from stocks.objects.abc import BaseEntity


class Payment(BaseEntity):
    """Dividend payment."""

    def __init__(
        self, ticker: str, declaration_date: datetime.date,
        amount: decimal.Decimal, source: str, is_forecast: bool,
    ):
        """Primary constructor."""
        self._ticker = ticker
        self._declaration_date = declaration_date
        self._amount = amount
        self._source = source
        self._is_forecast = is_forecast

    @classmethod
    def as_model(cls) -> flask_restx.Model:
        """As a swagger model."""
        return flask_restx.Model('Payment', {
            'ticker': flask_restx.fields.String(
                required=True,
                description='code of ticker',
                example='SBER',
            ),
            'declaration_date': flask_restx.fields.String(
                required=True,
                example='2020-04-01',
            ),
            'amount': flask_restx.fields.Fixed(
                required=True,
            ),
            'source': flask_restx.fields.String(
                required=True,
                description='source from which payment was crawled.',
                example='smartlab',
            ),
            'is_forecast': flask_restx.fields.Boolean(
                required=True,
                description='if true then this payment is a forecast.',
                example=False,
            ),
        })

    def as_dict(self):
        """Serialize payment details."""
        return {
            'ticker': self._ticker,
            'declaration_date': self._declaration_date.strftime('%Y-%m-%d'),
            'amount': self._amount,
            'source': self._source,
            'is_forecast': self._is_forecast,
        }


PaymentModel = Payment.as_model()
