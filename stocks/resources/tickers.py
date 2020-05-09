"""A set of resources that works with tickers."""
import flask_restplus

import stocks.types


class TickersResource(flask_restplus.Resource):
    """Basic resource that works with stock tickers."""

    def get(self) -> stocks.types.ResponseListType:
        """Return list of available tickers."""
        return {'results': [], 'count': 0}
