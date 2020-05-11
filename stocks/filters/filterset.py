"""Classes that helps to filter mongo collections."""
import typing

from stocks.filters.fields import BaseField
from stocks.filters.query import Query, QueryValue


class FilterSetMeta(type):
    """Basic meta class for filter classes."""

    def __new__(cls, name, bases, attrs):
        """Move all field instances to a separate `fields` attribute."""
        attrs['fields'] = {}
        for attr, obj in attrs.copy().items():
            if isinstance(obj, BaseField):
                attrs['fields'][attr] = attrs.pop(attr)
        return super(FilterSetMeta, cls).__new__(cls, name, bases, attrs)


class BaseFilterSet(metaclass=FilterSetMeta):
    """Base filter class.

    It does two main things:
    1) provides doc schemas for swagger.
    2) builds a mongo db query based on query params.
    """

    fields: typing.Dict[str, BaseField]

    def __init__(self, args: typing.Dict[str, str]):
        """Primary constructor.

        Args:
            args (dict): query params from request
        """
        self.args = args

    @classmethod
    def as_params(cls) -> typing.Dict[str, typing.Dict[str, str]]:
        """Return a schema acceptable for swagger docs."""
        return {name: field.schema() for name, field in cls.fields.items()}

    def query(self) -> Query:
        """Return mongodb query based in filter fields."""
        result: typing.Dict[str, QueryValue] = {}

        for key, value in self.args.items():
            if key in self.fields:
                field = self.fields[key]
                result[key] = {field.operator(): field.clean(value)}

        return Query(result)
