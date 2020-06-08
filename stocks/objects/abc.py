"""Base interfaces."""
import abc
import typing

import flask_restx


class BaseEntity(metaclass=abc.ABCMeta):
    """Base class for domain entity."""

    @abc.abstractmethod
    def as_dict(self) -> typing.Dict[str, typing.Any]:
        """Serialize entity."""

    @abc.abstractclassmethod
    def as_model(self) -> flask_restx.Model:
        """Make swagger model from entity."""
