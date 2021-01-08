"""Routes to work with auth tokens."""
import fastapi

from stocks import dependendies
from stocks.entities import Token
from stocks.repositories import UoW


router = fastapi.APIRouter()


@router.post('', response_model=Token)
async def create_token(
    uow: UoW = fastapi.Depends(dependendies.get_uow),
) -> Token:
    """Return the list of available tickers."""
    with uow:
        token = Token.generate()
        uow.tokens.add(token)
        uow.commit()

    return token
