"""Router to work with portfolio."""
import collections
import typing

import fastapi
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from stocks import dependendies, responses
from stocks.entities import (PfAction, PfOperation, PfOperationBase,
                             PfOperationCreate, PfPosition, PfSummary,
                             TokenCode)
from stocks.repositories import UoW


router = fastapi.APIRouter()

http_bearer = HTTPBearer()


def get_portfolio_token(
    uow: UoW = fastapi.Depends(dependendies.get_uow),
    creds: HTTPAuthorizationCredentials = fastapi.Depends(http_bearer),
) -> str:
    """Check if token exists."""
    with uow:
        tokens = uow.tokens.iterator({'token': creds.credentials})

    if not list(tokens):
        raise fastapi.HTTPException(status_code=403, detail='Invalid token.')

    return creds.credentials


@router.post('/operations', response_model=responses.Ok)
async def create_operation(
    operation: PfOperationBase,
    token: TokenCode = fastapi.Depends(get_portfolio_token),
    uow: UoW = fastapi.Depends(dependendies.get_uow),
) -> responses.Ok:
    """Create a new operation."""
    to_create = PfOperationCreate(token=token, **operation.dict())

    with uow:
        uow.pf_operations.add(to_create)
        uow.commit()

    return responses.Ok()


@router.get('/operations', response_model=responses.ListResponse[PfOperation])
async def operations(
    token: TokenCode = fastapi.Depends(get_portfolio_token),
    uow: UoW = fastapi.Depends(dependendies.get_uow),
) -> responses.ListResponse[PfOperation]:
    """Return the list of operations."""
    with uow:
        results = uow.pf_operations.iterator({'token': token})

    return responses.ListResponse(results=results)


@router.get('/summary', response_model=PfSummary)
async def summary(
    token: TokenCode = fastapi.Depends(get_portfolio_token),
    uow: UoW = fastapi.Depends(dependendies.get_uow),
) -> PfSummary:
    """Return the list of operations."""
    with uow:
        operations = uow.pf_operations.iterator({'token': token})

    counter: typing.Counter[str] = collections.Counter()

    for operation in operations:
        if operation.action == PfAction.buy:
            counter[operation.ticker] += operation.quantity

        if operation.action == PfAction.sell:
            counter[operation.ticker] -= operation.quantity

    return PfSummary(
        positions=[
            PfPosition(ticker=ticker, quantity=quantity)
            for ticker, quantity in counter.items()
        ],
    )
