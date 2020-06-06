"""Classes to work with storage."""
import abc

from stocks.filters.query import Query


class BaseRepository(metaclass=abc.ABCMeta):
    """Base interface to interact with db."""

    @abc.abstractclassmethod
    def search(self, query: Query) -> list:
        """Search entities in db."""

    @abc.abstractclassmethod
    def drop(self, query: Query):
        """Drop entities."""

    @abc.abstractmethod
    def add_bulk(self, objects: list):
        """Add batch of entities."""

    def recreate(self, objects: list):
        """Drop all entities and create new."""
        self.drop(Query({}))
        self.add_bulk(objects)


class TickerRepository(BaseRepository):
    """Base repository to work with tickers."""

    def __init__(self, db):
        """Primary constructor."""
        self._db = db

    def search(self, query: Query):
        """Search for tickers."""
        return list(self._db.tickers.find(query))

    def drop(self, query: Query):
        """Drop tickers."""
        self._db.tickers.drop(query)

    def add_bulk(self, objects: list):
        """Add batch of tickers."""
        self._db.tickers.insert_many(objects)


class PaymentRepository(BaseRepository):
    """Base repository to work with payments."""

    def __init__(self, db):
        """Primary constructor."""
        self._db = db

    def search(self, query: Query):
        """Search for payments."""
        return list(self._db.payments.find(query))

    def drop(self, query: Query):
        """Drop payments."""
        self._db.payments.drop(query)

    def add_bulk(self, objects: list):
        """Add batch of tickers."""
        self._db.payments.insert_many(objects)


class QuoteRepository(BaseRepository):
    """Base repository to work with historical quotes."""

    def __init__(self, db):
        """Primary constructor."""
        self._db = db

    def search(self, query: Query):
        """Search for quotes."""
        return list(self._db.quotes.find(query))

    def drop(self, query: Query):
        """Drop payments."""
        self._db.quotes.drop(query)

    def add_bulk(self, objects: list):
        """Add batch of tickers."""
        self._db.quotes.insert_many(objects)
