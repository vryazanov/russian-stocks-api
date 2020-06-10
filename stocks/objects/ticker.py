"""Ticker object."""
import typing

import flask_restx
import flask_restx.fields

from stocks.objects.abc import ANY_PRIMITIVE, BaseEntity


class Ticker(BaseEntity):
    """Ticker."""

    def __init__(self, name: str, code: str):
        """Primary constructor."""
        self._name = name
        self._code = code

    @classmethod
    def as_model(cls) -> flask_restx.Model:
        """Build swagger model."""
        return flask_restx.Model('Ticker', {
            'name': flask_restx.fields.String(
                required=True,
                example='Sberbank',
            ),
            'ticker': flask_restx.fields.String(
                required=True,
                description='code of ticker',
                example='SBER',
            ),
        })

    def as_dict(self) -> typing.Dict[str, ANY_PRIMITIVE]:
        """Serialize ticker."""
        return {
            'name': self._name,
            'ticker': self._code,
        }


TickerModel = Ticker.as_model()
