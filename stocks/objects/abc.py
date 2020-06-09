"""Base interfaces."""
import abc
import typing

import flask_restx


ANY_PRIMITIVE = typing.Optional[typing.Union[str, int, bool]]


class BaseEntity(metaclass=abc.ABCMeta):
    """Base class for domain entity."""

    @abc.abstractmethod
    def as_dict(self) -> typing.Dict[str, ANY_PRIMITIVE]:
        """Serialize entity."""

    @abc.abstractclassmethod
    def as_model(self) -> flask_restx.Model:
        """Make swagger model from entity."""
