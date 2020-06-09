"""Custom namespace for flask-restx."""
import typing

import flask_restx

from stocks.objects.abc import BaseEntity


class Namespace(flask_restx.Namespace):
    """It's introduced to add some methods to work with entitites."""

    def marshal_entity_with(self, fields: flask_restx.Model, **kwargs):
        """Behave like `matshal_list_with` but unpack single entity."""
        def outer(f):
            def inner(*args, **kwargs):
                return f(*args, **kwargs).as_dict()
            return self.marshal_with(fields, False, **kwargs)(inner)
        return outer

    def marshal_entities_list_with(self, fields: flask_restx.Model, **kwargs):
        """Behave like `matshal_list_with` but unpack entities."""
        def outer(f):
            def inner(*args, **kwargs):
                entities: typing.List[BaseEntity] = f(*args, **kwargs)
                return [entity.as_dict() for entity in entities]
            return self.marshal_with(fields, True, **kwargs)(inner)
        return outer
