"""Objects to work with portfolio."""
import datetime
import decimal
import typing

import flask_restx
import flask_restx.fields

from stocks.filters.query import AssetQuery
from stocks.objects.abc import BaseEntity
from stocks.rest_fields import Fixed


if typing.TYPE_CHECKING:
    from stocks.repostories import Assets


class Portfolio(BaseEntity):
    """Portfolio object."""

    START_YEAR = 2015

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
        today = datetime.datetime.today()
        return {
            'payments': [
                {
                    'year': year,
                    'amount': float(self.dividends_within_date_range(
                        'dohod',
                        datetime.date(year, 1, 1),
                        datetime.date(year + 1, 1, 1),
                    )),
                } for year in range(self.START_YEAR, today.year + 1)
            ],
        }


YearPaymentModel = flask_restx.Model('YearPayment', {
    'year': flask_restx.fields.Integer(),
    'amount': Fixed(decimals=2),
})

PortfolioModel = Portfolio.as_model()
