"""Flask entrypoint."""
import os

import dotenv
import flask
import flask_restplus
import pymongo
import pymongo.uri_parser
from werkzeug.middleware.proxy_fix import ProxyFix

from stocks import models
from stocks.resources import imports, tickers


dotenv.load_dotenv()


def create_app() -> flask.Flask:
    """Create and return flask application."""
    app = flask.Flask(__name__)
    app.config.from_object(os.environ['FLASK_CONFIG'])

    app.api = init_api(app)
    app.mongo = init_mongo(app)

    app.wsgi_app = ProxyFix(app.wsgi_app)  # type: ignore
    return app


def init_api(app: flask.Flask) -> flask_restplus.Api:
    """Initialize api."""
    api = flask_restplus.Api()

    api.init_app(app)

    api.add_namespace(tickers.ns)
    api.add_namespace(imports.ns)

    api.add_model(models.Ticker.name, models.Ticker)
    api.add_model(models.HistoricalQuote.name, models.HistoricalQuote)
    api.add_model(models.Payment.name, models.Payment)

    return api


def init_mongo(app: flask.Flask) -> pymongo.MongoClient:
    """Initialize mongo client."""
    return pymongo.MongoClient(app.config['MONGODB_URI'], retryWrites=False)
