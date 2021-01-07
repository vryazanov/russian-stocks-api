"""Base interfaces for repositories."""
import abc
import typing


EntityT = typing.TypeVar('EntityT')
EntityBaseT = typing.TypeVar('EntityBaseT', contravariant=True)
EntityCreateT = typing.TypeVar('EntityCreateT', contravariant=True)

FilterT = typing.TypeVar('FilterT', contravariant=True)


class BaseRepository(
    typing.Protocol[
        EntityT,
        EntityBaseT,
        EntityCreateT,
        FilterT,
    ], metaclass=abc.ABCMeta,
):
    """Base class for repository."""

    @abc.abstractmethod
    def add(self, entity: EntityCreateT) -> None:
        """Add a new entity."""

    @abc.abstractmethod
    def exists(self, entity: EntityBaseT) -> bool:
        """Return true if entity exists."""

    @abc.abstractmethod
    def iterator(self, filters: FilterT) -> typing.List[EntityT]:
        """Return iterator over entities."""


TickerRepositoryT = typing.TypeVar('TickerRepositoryT')
PaymentRepositoryT = typing.TypeVar('PaymentRepositoryT')
QuoteRepositoryT = typing.TypeVar('QuoteRepositoryT')


class BaseUnitOfWork(
    typing.Protocol[
        TickerRepositoryT,
        PaymentRepositoryT,
        QuoteRepositoryT,
    ], metaclass=abc.ABCMeta,
):
    """Base unit of work."""

    tickers: TickerRepositoryT
    payments: PaymentRepositoryT
    quotes: QuoteRepositoryT

    def __exit__(self) -> None:
        """Rollback transaction in case of exceptions."""
        self.rollback()

    @abc.abstractmethod
    def __enter__(self) -> None:
        """Start transaction."""

    @abc.abstractmethod
    def commit(self) -> None:
        """Commit transaction."""

    @abc.abstractmethod
    def rollback(self) -> None:
        """Rollback transaction."""
