"""Token repository."""
import typing

import sqlalchemy.orm
import typing_extensions

from stocks import db
from stocks.entities import Token
from stocks.repositories.abc import BaseRepository


class TokenFilters(typing_extensions.TypedDict):
    """Possible filters for tokens."""

    token: str


class Tokens(
    BaseRepository[
        Token,
        Token,
        Token,
        TokenFilters,
    ],
):
    """Tokens repository."""

    def __init__(self, session: sqlalchemy.orm.Session):
        """Primary constructor."""
        self._session = session

    def exists(self, entity: Token) -> bool:
        """Return true if token exists."""
        return bool(
            self._session.query(db.TokenModel).filter(
                db.TokenModel.token == entity.token,
            ).first(),
        )

    def add(self, entity: Token) -> None:
        """Save token to db."""
        self._session.add(db.TokenModel(token=entity.token))

    def iterator(self, filters: TokenFilters) -> typing.List[Token]:
        """Return list of tokens."""
        query = self._session.query(db.TokenModel).all()
        return [Token.from_orm(token) for token in query]
