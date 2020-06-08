"""Objects to work with investment portfolio."""
from stocks.objects.ticker import Ticker


class Assets:
    """Investment assets."""

    def __init__(self, ticker: Ticker, quantity: int):
        """Primary constructor."""
        self._ticker = ticker
        self._quantity = quantity
