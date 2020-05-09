"""Flask entrypoint."""
import os

import flask
import flask_restplus
import pymongo
import pymongo.uri_parser
import werkzeug.middleware.proxy_fix

from stocks.resources import tickers


def create_app() -> flask.Flask:
    """Create and return flask application."""
    app = flask.Flask(__name__)
    app.config.from_object(os.environ['FLASK_CONFIG'])

    app.api = init_api(app)
    app.mongo = init_mongo(app)

    app.wsgi_app = werkzeug.middleware.proxy_fix.ProxyFix(app.wsgi_app)  # type: ignore
    return app


def init_api(app: flask.Flask) -> flask_restplus.Api:
    """Initialize api."""
    api = flask_restplus.Api()

    api.init_app(app)
    api.add_namespace(tickers.ns)

    return api


def init_mongo(app: flask.Flask) -> pymongo.MongoClient:
    """Initialize mongo client."""
    return pymongo.MongoClient(app.config['MONGODB_URI'], retryWrites=False)
