"""A set of types of filters package."""
from __future__ import annotations

import collections
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

    def equal_to(self, **kwargs) -> Query:
        """Add `$eq` operation for provided kwargs."""
        for key, value in kwargs.items():
            self[key] = {'$eq': value}
        return self
