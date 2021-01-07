"""Unit of works."""
from stocks.entities import Ticker, Payment
from stocks.repositories.abc import BaseUnitOfWork
from stocks.repositories.tickers import Tickers
from stocks.repositories.payments import Payments


class SqlUoW(BaseUnitOfWork[Ticker, Payment]):
    """SQL unit of work."""

    def __init__(self, session_factory):
        """Primary constructor."""
        self.session_factory = session_factory

    def __enter__(self):
        """Create a db session and initialize repositories."""
        self.session = self.session_factory()
        self.tickers = Tickers(self.session)
        self.payments = Payments(self.session)

    def __exit__(self, *args, **kwargs) -> None:
        """Close db session."""
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        """Commit sql transaction."""
        self.session.commit()

    def rollback(self):
        """Rollback sql transaction."""
        self.session.rollback()
