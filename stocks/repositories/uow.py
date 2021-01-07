"""Unit of works."""
import typing

import sqlalchemy.orm

from stocks.repositories.abc import BaseUnitOfWork
from stocks.repositories.operations import PfOperations
from stocks.repositories.payments import Payments
from stocks.repositories.quotes import Quotes
from stocks.repositories.tickers import Tickers
from stocks.repositories.tokens import Tokens


class UoW(BaseUnitOfWork[Tickers, Payments, Quotes]):
    """SQL unit of work."""

    def __init__(self, session_factory: sqlalchemy.orm.sessionmaker) -> None:
        """Primary constructor."""
        self.session_factory = session_factory

    def __enter__(self) -> None:
        """Create a db session and initialize repositories."""
        self.session = self.session_factory()
        self.tickers = Tickers(self.session)
        self.payments = Payments(self.session)
        self.quotes = Quotes(self.session)
        self.tokens = Tokens(self.session)
        self.pf_operations = PfOperations(self.session)

    def __exit__(self, *args: typing.List[typing.Any]) -> None:
        """Close db session."""
        super().__exit__()
        self.session.close()

    def commit(self) -> None:
        """Commit sql transaction."""
        self.session.commit()

    def rollback(self) -> None:
        """Rollback sql transaction."""
        self.session.rollback()
