"""Repositories for portfolio operations."""
import typing

import sqlalchemy.orm
import typing_extensions

from stocks import db
from stocks.entities import PfOperation, PfOperationCreate
from stocks.repositories.abc import BaseRepository


class PfOperationFilters(typing_extensions.TypedDict):
    """Possible filters for portfolio operations."""

    token: str


class PfOperations(
    BaseRepository[
        PfOperation,
        PfOperation,
        PfOperationCreate,
        PfOperationFilters,
    ],
):
    """Portfolio operations repository."""

    def __init__(self, session: sqlalchemy.orm.Session):
        """Primary constructor."""
        self._session = session

    def exists(self, entity: PfOperation) -> bool:
        """Return true if operation exists."""
        return bool(
            self._session.query(db.PfOperationModel).filter(
                db.PfOperationModel.id == entity.id,
            ).first(),
        )

    def add(self, entity: PfOperationCreate) -> None:
        """Save ticker to db."""
        self._session.add(
            db.PfOperationModel(
                ticker=entity.ticker,
                token=entity.token,
                action=entity.action,
                quantity=entity.quantity,
                price=float(entity.price),
            ),
        )

    def iterator(self, filters: PfOperationFilters) -> typing.List[PfOperation]:  # noqa
        """Return list of portfolio operations."""
        query = self._session.query(db.PfOperationModel).filter(
            db.PfOperationModel.token == filters['token'],
        )
        return [PfOperation.from_orm(operation) for operation in query]
