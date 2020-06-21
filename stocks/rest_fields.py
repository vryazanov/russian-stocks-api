"""Custom wrappers around flask_restx fields."""
import flask_restx.fields


class Fixed(flask_restx.fields.Fixed):
    """Works the same as base class, but returns float."""

    def format(self, value):
        """Make it float."""
        return float(super().format(value))
