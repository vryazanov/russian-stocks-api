"""A set of application filter sets.

They are used to filted mongo collections by query params.
"""
from flask_restx import fields

from stocks.filters import BaseFilterSet, BoleanField, EqualField


class TickersFilterSet(BaseFilterSet):
    """Possible fields to filter tickers."""

    ticker = EqualField(fields.String())


class PaymentsFilterSet(BaseFilterSet):
    """Possible fields to filter payments."""

    source = EqualField(fields.String())
    is_forecast = BoleanField(fields.Boolean())


class QuoteFilterSet(BaseFilterSet):
    """Possible fields to filter stock quotes."""

    date = EqualField(fields.String())
