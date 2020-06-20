"""A set of types of filters package."""
from __future__ import annotations

import collections
import datetime
import typing


QueryValue = typing.Dict[str, typing.Union[str, int, bool]]
QueryType = typing.Dict[str, QueryValue]


if typing.TYPE_CHECKING:
    TypedUserDict = collections.UserDict[str, QueryValue]
else:
    TypedUserDict = collections.UserDict


class Query(TypedUserDict):
    """Dict representation of mongodb query."""

    def __init__(self, data: typing.Optional[QueryType] = None):
        """Primary constructor."""
        self.data = data or {}

    def _set_operator(self, operator: str, **kwargs) -> Query:
        """Update query."""
        for key, value in kwargs.items():
            self[key] = {operator: value}
        return self

    def equal_to(self, **kwargs) -> Query:
        """Add `$eq` operation for provided kwargs."""
        return self._set_operator('$eq', **kwargs)

    def greater_than(self, **kwargs) -> Query:
        """Add `$gt` operation for provided kwargs."""
        return self._set_operator('$gt', **kwargs)

    def less_than(self, **kwargs) -> Query:
        """Add `$lt` operation for provided kwargs."""
        return self._set_operator('$lt', **kwargs)


class PaymentQuery(Query):
    """Payment specific query."""

    def within_date_range(
        self, ticker: str, date_from: datetime.date, date_to: datetime.date,
    ):
        """Return query that contains payments declared within date range."""
        return self.equal_to(
            ticker=ticker,
        ).greater_than(
            declaration_date=date_from.strftime('%Y-%-m-%d'),
        ).less_than(
            declaration_date=date_to.strftime('%Y-%-m-%d'),
        )


class AssetQuery(Query):
    """Asset specific query."""

    def belong_to(self, owner: str):
        """Return query that contains assets which belong to specific user."""
        return self.equal_to(owner=owner)
