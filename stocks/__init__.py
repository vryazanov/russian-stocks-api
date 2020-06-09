"""Flask entrypoint."""
import os

import dotenv
import flask
import flask_restx
import pymongo
import pymongo.uri_parser
from werkzeug.middleware.proxy_fix import ProxyFix

from stocks import models
from stocks.objects.payment import PaymentModel
from stocks.objects.token import TokenModel
from stocks.resources import imports, portfolio, tickers, tokens


dotenv.load_dotenv()


def create_app() -> flask.Flask:
    """Create and return flask application."""
    app = flask.Flask(__name__)
    app.config.from_object(os.environ['FLASK_CONFIG'])

    app.api = init_api(app)
    app.mongo = init_mongo(app)

    app.wsgi_app = ProxyFix(app.wsgi_app)  # type: ignore
    return app


def init_api(app: flask.Flask) -> flask_restx.Api:
    """Initialize api."""
    api = flask_restx.Api(authorizations={
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'X-Authorization',
        },
    })

    api.init_app(app)

    api.add_namespace(tokens.ns)
    api.add_namespace(portfolio.ns)
    api.add_namespace(tickers.ns)
    api.add_namespace(imports.ns)

    api.add_model(models.Ticker.name, models.Ticker)
    api.add_model(models.HistoricalQuote.name, models.HistoricalQuote)
    api.add_model(PaymentModel.name, PaymentModel)
    api.add_model(TokenModel.name, TokenModel)

    return api


def init_mongo(app: flask.Flask) -> pymongo.MongoClient:
    """Initialize mongo client."""
    return pymongo.MongoClient(app.config['MONGODB_URI'], retryWrites=False)
