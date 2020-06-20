"""Application containers."""
import dependencies
import flask
import pymongo

from stocks.repostories import Assets, Payments, Quotes, Tickers, Tokens


def get_db() -> pymongo.MongoClient:
    """Return mongo client from current app."""
    return flask.current_app.mongo.get_database()


class Repositories(dependencies.Injector):
    """Repositories container."""

    db = dependencies.value(get_db)

    assets = Assets
    quotes = Quotes
    tokens = Tokens
    tickers = Tickers
    payments = Payments
