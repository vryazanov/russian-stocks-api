"""A set of application filter sets.

They are used to filted mongo collections by query params.
"""
from stocks import models
from stocks.filters import BaseFilterSet, BoleanField, EqualField


class TickersFilterSet(BaseFilterSet):
    """Possible fields to filter tickers."""

    ticker = EqualField(models.Ticker['ticker'])


class PaymentsFilterSet(BaseFilterSet):
    """Possible fields to filter payments."""

    source = EqualField(models.Payment['source'])
    is_forecast = BoleanField(models.Payment['is_forecast'])


class QuoteFilterSet(BaseFilterSet):
    """Possible fields to filter stock quotes."""

    date = EqualField(models.HistoricalQuote['date'])
