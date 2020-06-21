"""Objects to work with portfolio."""
import datetime
import decimal
import typing

import flask_restx
import flask_restx.fields

from stocks.filters.query import AssetQuery
from stocks.objects.abc import ANY_PRIMITIVE, BaseEntity


if typing.TYPE_CHECKING:
    from stocks.repostories import Assets


class Portfolio(BaseEntity):
    """Portfolio object."""

    def __init__(self, owner: str, assets: 'Assets'):
        """Primary constructor."""
        self._owner = owner
        self._assets = assets

    def dividends_within_date_range(
        self, source: str, date_from: datetime.date, date_to: datetime.date,
    ) -> decimal.Decimal:
        """Calculate amount of dividends within date range."""
        amount = decimal.Decimal()

        for asset in self._assets.search(
            AssetQuery().belong_to(self._owner),
        ):
            amount += asset.dividends_within_date_range(date_from, date_to)

        return amount

    @classmethod
    def as_model(cls) -> flask_restx.Model:
        """Build swagger model."""
        return flask_restx.Model('Portfolio', {
            'payments': flask_restx.fields.Nested(
                model=YearPaymentModel, as_list=True),
        })

    def as_dict(self) -> typing.Dict[str, typing.Any]:  # type: ignore
        """Serialize portfolio."""
        return {
            'payments': [
                {
                    'year': 2020,
                    'amount': float(self.dividends_within_date_range(
                        'smartlab',
                        datetime.date(2020, 1, 1),
                        datetime.date(2021, 1, 1),
                    )),
                },
            ],
        }


YearPaymentModel = flask_restx.Model('YearPayment', {
    'year': flask_restx.fields.Integer(),
    'amount': flask_restx.fields.Fixed(decimals=2),
})

PortfolioModel = Portfolio.as_model()
