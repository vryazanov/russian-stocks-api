"""Flask entrypoint."""
import flask
import flask_restplus

import stocks.resources


def create_app() -> flask.Flask:
    """Create and return flask application."""
    app = flask.Flask(__name__)

    init_api(app)

    return app


def init_api(app: flask.Flask) -> flask_restplus.Api:
    """Initialize api and setup routing."""
    api = flask_restplus.Api()
    api.add_resource(stocks.resources.TickersResource, '/tickers')
    api.init_app(app)
