"""Router to work with portfolio."""
import fastapi
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from stocks import dependendies, responses
from stocks.entities import (PfOperation, PfOperationBase, PfOperationCreate,
                             TokenCode,)
from stocks.repositories.uow import UoW


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


@router.post(
    '/operations',
    response_model=responses.Ok,
    operation_id='perform_operation',
)
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


@router.get(
    '/operations',
    response_model=responses.ListResponse[PfOperation],
    operation_id='list_operations',
)
async def operations(
    token: TokenCode = fastapi.Depends(get_portfolio_token),
    uow: UoW = fastapi.Depends(dependendies.get_uow),
) -> responses.ListResponse[PfOperation]:
    """Return the list of operations."""
    with uow:
        results = uow.pf_operations.iterator({'token': token})

    return responses.ListResponse(results=results)
