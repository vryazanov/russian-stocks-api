"""Flask entrypoint."""
import os

import dotenv
import flask
import flask_restx
import pymongo
import pymongo.uri_parser
from werkzeug.middleware.proxy_fix import ProxyFix

from stocks.objects.asset import AssetModel
from stocks.objects.payment import PaymentModel
from stocks.objects.portfolio import PortfolioModel, YearPaymentModel
from stocks.objects.quote import QuoteModel
from stocks.objects.ticker import TickerModel
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

    api.add_model(TickerModel.name, TickerModel)
    api.add_model(QuoteModel.name, QuoteModel)
    api.add_model(PaymentModel.name, PaymentModel)
    api.add_model(TokenModel.name, TokenModel)
    api.add_model(PortfolioModel.name, PortfolioModel)
    api.add_model(YearPaymentModel.name, YearPaymentModel)
    api.add_model(AssetModel.name, AssetModel)

    return api


def init_mongo(app: flask.Flask) -> pymongo.MongoClient:
    """Initialize mongo client."""
    return pymongo.MongoClient(app.config['MONGODB_URI'], retryWrites=False)
