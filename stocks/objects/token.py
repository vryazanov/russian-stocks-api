"""Objects to work with tokens."""
from __future__ import annotations

import secrets
import typing

import flask_restx
import flask_restx.fields

from stocks.objects.abc import ANY_PRIMITIVE, BaseEntity


class Token(BaseEntity):
    """User token."""

    def __init__(self, secret_key: str):
        """Primary constructor."""
        self._secret_key = secret_key

    @classmethod
    def generate(cls) -> Token:
        """Generate secret key and build an instance."""
        return cls(secret_key=secrets.token_hex(32))

    @classmethod
    def as_model(cls) -> flask_restx.Model:
        """Swagger model."""
        return flask_restx.Model('Token', {
            'secret_key': flask_restx.fields.String(),
        })

    def as_dict(self) -> typing.Dict[str, ANY_PRIMITIVE]:
        """Serialize token."""
        return {
            'secret_key': self._secret_key,
        }


TokenModel = Token.as_model()
