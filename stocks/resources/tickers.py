"""A set of resources that works with tickers."""
import flask_restplus


class TickersResource(flask_restplus.Resource):
    """Basic resource that works with stock tickers."""

    def get(self) -> dict:
        """Return list of available tickers."""
        return {'results': []}
