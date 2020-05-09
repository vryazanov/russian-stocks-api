"""Custom application types."""
import typing

import typing_extensions


class ResponseListType(typing_extensions.TypedDict):
    """Basic type for every responses with a list of objects."""

    count: int
    results: typing.List[typing.Dict[str, typing.Any]]
