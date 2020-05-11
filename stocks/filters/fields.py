"""A set of fields for filter classes."""
import abc
import typing

import flask_restplus.fields


class BaseField(metaclass=abc.ABCMeta):
    """Basic field for filter set class."""

    @abc.abstractmethod
    def operator(self) -> str:
        """Return mongodb operator, `$eq` as an example."""

    @abc.abstractmethod
    def schema(self) -> typing.Dict[str, str]:
        """Return schema of encapsulated field."""

    @abc.abstractmethod
    def clean(self, value: str):
        """Return cleaned value that will be passed to mongo."""


class BaseModelField(BaseField):
    """Add functionality to work with `flask_restplus.Model`."""

    def __init__(self, field: flask_restplus.fields.Raw):
        """Primary constructor.

        Take only model's field for swagger docs.
        """
        self.field = field

    def schema(self) -> typing.Dict[str, str]:
        """Return description for swagger docs."""
        return self.field.schema()


class EqualField(BaseModelField):
    """Field that provides exact equal."""

    def operator(self) -> str:
        """Return mongo's equal operator."""
        return '$eq'

    def clean(self, value: str):
        """Return value as is."""
        return value


class BoleanField(BaseModelField):
    """It does the same as EqualField, but cleans value to bool."""

    TRUE_VALUES = ('true', 't', '1', 'y', 'yes')

    def operator(self) -> str:
        """Return mongo's equal operator."""
        return '$eq'

    def clean(self, value: str) -> bool:
        """Check if provided value is bool or not.

        >>> BoleanField('some description').clean('True')
        True
        >>> BoleanField('some description').clean('0')
        False
        """
        return value.strip().lower() in self.TRUE_VALUES
