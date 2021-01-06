"""Schemas for api responses."""
import typing

import pydantic
import pydantic.generics


EntityT = typing.TypeVar('EntityT')


class Ok(pydantic.BaseModel):
    """Ok."""

    success: bool = True


class ListResponse(pydantic.generics.GenericModel, typing.Generic[EntityT]):
    """Listing response."""

    results: typing.List[EntityT]
