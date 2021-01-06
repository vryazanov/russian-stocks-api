"""Routes for importing data."""
import typing

import fastapi
import fastapi.security
import pymongo

from stocks import responses, settings
from stocks.entities import Payment, Ticker
from stocks.mongo import get_mongo


router = fastapi.APIRouter()

http_bearer = fastapi.security.HTTPBearer()


def check_import_token(
    auth: fastapi.security.HTTPBearer = fastapi.Depends(http_bearer),
    settings: settings.Settings = fastapi.Depends(settings.get_settings),
):
    """Check if token has permission to import data."""
    if auth.credentials != settings.import_token:
        raise fastapi.HTTPException(status_code=403, detail='Invalid token.')


@router.post(
    '/tickers/',
    response_model=responses.Ok,
    operation_id='import_tickers',
    summary='Import tickers.',
    dependencies=[fastapi.Depends(check_import_token)],
)
async def tickers(
    tickers: typing.List[Ticker],
    mongo: pymongo.MongoClient = fastapi.Depends(get_mongo),
) -> typing.List[Ticker]:
    """Take a list of tickers and save to db."""
    mongo.db.tickers.insert_many([ticker.to_mongo() for ticker in tickers])
    return responses.Ok()


@router.post(
    '/payments/',
    response_model=responses.Ok,
    operation_id='import_payments',
    summary='Import dividend payments.',
    dependencies=[fastapi.Depends(check_import_token)],
)
async def payments(
    payments: typing.List[Payment],
    mongo: pymongo.MongoClient = fastapi.Depends(get_mongo),
) -> typing.List[Ticker]:
    """Take a list of tickers and save to db."""
    mongo.db.payments.insert_many([payment.to_mongo() for payment in payments])
    return responses.Ok()
