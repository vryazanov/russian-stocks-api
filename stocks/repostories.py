"""Classes to work with storage."""
import abc
import datetime
import decimal
import typing

import pymongo.database

from stocks.filters.query import Query
from stocks.objects.abc import BaseEntity
from stocks.objects.asset import Asset
from stocks.objects.payment import Payment
from stocks.objects.quote import Quote
from stocks.objects.ticker import Ticker
from stocks.objects.token import Token


LIST_OF_DICTS = typing.List[typing.Dict[str, typing.Any]]  # type: ignore


class BaseRepository(metaclass=abc.ABCMeta):
    """Base interface to interact with db."""

    @abc.abstractclassmethod
    def search(self, query: Query) -> typing.List[BaseEntity]:
        """Search entities in db."""

    @abc.abstractclassmethod
    def drop(self, query: Query):
        """Drop entities."""


class RecreatableRepository(BaseRepository):
    """Add some methods to work with bulk of entities."""

    @abc.abstractmethod
    def add_bulk(self, objects: LIST_OF_DICTS):
        """Add batch of entities."""

    def recreate(self, objects: LIST_OF_DICTS):
        """Drop all entities and create new."""
        self.drop(Query())
        self.add_bulk(objects)


class Tickers(RecreatableRepository):
    """Base repository to work with tickers."""

    def __init__(self, db: pymongo.database.Database):
        """Primary constructor."""
        self._db = db

    def search(self, query: Query) -> typing.List[BaseEntity]:
        """Search for tickers."""
        return [
            Ticker(
                name=ticker['name'],
                code=ticker['ticker'],
            ) for ticker in self._db.tickers.find(query)]

    def drop(self, query: Query):
        """Drop tickers."""
        self._db.tickers.drop(query)

    def add_bulk(self, objects: LIST_OF_DICTS):
        """Add batch of tickers."""
        self._db.tickers.insert_many(objects)


class Payments(RecreatableRepository):
    """Base repository to work with payments."""

    def __init__(self, db: pymongo.database.Database):
        """Primary constructor."""
        self._db = db

    def search(self, query: Query) -> typing.List[BaseEntity]:
        """Search for payments."""
        return [Payment(
            ticker=payment['ticker'],
            declaration_date=datetime.datetime.strptime(
                payment['declaration_date'], '%Y-%m-%d'),
            amount=decimal.Decimal(payment['amount']),
            is_forecast=payment['is_forecast'],
            source=payment['source'],
        ) for payment in self._db.payments.find(query)]

    def drop(self, query: Query):
        """Drop payments."""
        self._db.payments.drop(query)

    def add_bulk(self, objects: LIST_OF_DICTS):
        """Add batch of tickers."""
        self._db.payments.insert_many(objects)


class Quotes(RecreatableRepository):
    """Base repository to work with historical quotes."""

    def __init__(self, db: pymongo.database.Database):
        """Primary constructor."""
        self._db = db

    def search(self, query: Query) -> typing.List[BaseEntity]:
        """Search for quotes."""
        return [
            Quote(
                ticker=quote['ticker'],
                date=datetime.datetime.strptime(quote['date'], '%Y-%m-%d'),
                open_price=decimal.Decimal(quote['open_price']),
                close_price=decimal.Decimal(quote['close_price']),
            ) for quote in self._db.quotes.find(query)]

    def drop(self, query: Query):
        """Drop payments."""
        self._db.quotes.drop(query)

    def add_bulk(self, objects: LIST_OF_DICTS):
        """Add batch of tickers."""
        self._db.quotes.insert_many(objects)


class Tokens(BaseRepository):
    """Repostitory to work with user tokens."""

    def __init__(self, db: pymongo.database.Database):
        """Primary constructor."""
        self._db = db

    def add(self, token: Token):
        """Add a token to db."""
        self._db.tokens.insert(token.as_dict())

    def drop(self, query: Query):
        """Drop tokens."""
        self._db.tokens.drop(query)

    def search(self, query: Query) -> typing.List[BaseEntity]:
        """Search for tokens."""
        return [
            Token(secret_key=token['secret_key'])
            for token in self._db.tokens.find(query)]


class Assets(BaseRepository):
    """Repository to work with assets."""

    def __init__(self, db: pymongo.database.Database):
        """Primary constructor."""
        self._db = db

    def add(self, asset: Asset):
        """Add asset to db."""
        self._db.assets.insert(asset.as_dict())

    def drop(self, query: Query):
        """Drop tokens."""
        self._db.assets.drop(query)

    def search(self, query: Query) -> typing.List[BaseEntity]:
        """Search for assets."""
        return [Asset(
            owner=asset['owner'],
            ticker=asset['ticker'],
            quantity=asset['quantity'],
        ) for asset in self._db.assets.find(query)]
