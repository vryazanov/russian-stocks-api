"""Base interfaces for repositories."""
import abc
import typing


EntityT = typing.TypeVar('EntityT', contravariant=True)


class BaseRepository(
    typing.Protocol[EntityT], metaclass=abc.ABCMeta,
):
    """Base class for repository."""

    @abc.abstractmethod
    def add(self, entity: EntityT):
        """Add a new entity."""

    @abc.abstractmethod
    def exists(self, entity: EntityT) -> bool:
        """Return true if entity exists."""


TickerT = typing.TypeVar('TickerT')
PaymentT = typing.TypeVar('PaymentT')


class BaseUnitOfWork(
    typing.Protocol[TickerT, PaymentT], metaclass=abc.ABCMeta,
):
    """Base unit of work."""

    tickers: BaseRepository[TickerT]
    payments: BaseRepository[PaymentT]

    def __exit__(self, *args, **kwargs) -> None:
        """Rollback transaction in case of exceptions."""
        self.rollback()

    @abc.abstractmethod
    def commit(self) -> None:
        """Commit transaction."""

    @abc.abstractmethod
    def rollback(self) -> None:
        """Rollback transaction."""
