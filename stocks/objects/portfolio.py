"""Objects to work with investment portfolio."""
import typing

from stocks.objects.assets import Assets


class Portfolio:
    """Investment portfolio."""

    def __init__(self, owner: str, assets: typing.List[Assets]):
        """Primary constructor."""
        self._owner = owner
        self._assets = assets
