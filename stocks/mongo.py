"""Mongo client."""
import fastapi
import pymongo

from stocks.settings import Settings, get_settings


def get_mongo(
    settings: Settings = fastapi.Depends(get_settings),
) -> pymongo.MongoClient:
    """Return an instance of mongo client."""
    return pymongo.MongoClient(settings.mongodb_uri, retryWrites=False)
