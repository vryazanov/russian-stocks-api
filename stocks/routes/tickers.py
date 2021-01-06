"""Routes for tickers api."""
import fastapi
import pymongo

from stocks.entities import Payment, Ticker
from stocks.mongo import get_mongo
from stocks.responses import ListResponse


router = fastapi.APIRouter()


@router.get(
    '',
    response_model=ListResponse[Ticker],
    operation_id='get_tickers',
)
async def tickers(
    mongo: pymongo.MongoClient = fastapi.Depends(get_mongo),
):
    """Return the list of available tickers."""
    query = mongo.db.tickers.find({})
    return ListResponse(results=list(query))


@router.get(
    '/{ticker}/payments',
    response_model=ListResponse[Payment],
    operation_id='get_payments',
)
async def payments(
    ticker: str, mongo: pymongo.MongoClient = fastapi.Depends(get_mongo),
):
    """Return the list of available tickers."""
    query = mongo.db.payments.find({'ticker': {'$eq': ticker}})
    return ListResponse(results=list(query))
