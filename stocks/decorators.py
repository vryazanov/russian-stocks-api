"""List of method decorators."""
import flask

from stocks.filters.query import Query
from stocks.repostories import Tokens


def admin_auth_required(f):
    """Check authorization token."""
    def wrapper(*args, **kwargs):
        auth_token = flask.request.headers.get('X-Authorization', '')
        if not auth_token:
            flask.abort(401, 'Authorization token is not provided.')
        elif auth_token != flask.current_app.config['AUTH_IMPORT_TOKEN']:
            flask.abort(403, 'Authorization token is not valid.')
        return f(*args, **kwargs)
    return wrapper


def auth_required(f):
    """Check that provided token exists in the db."""
    def wrapper(*args, **kwargs):
        auth_token = flask.request.headers.get('X-Authorization', '')

        if not auth_token:
            flask.abort(401, 'Authorization token is not provided.')

        query = Query().equal_to(secret_key=auth_token)

        tokens = Tokens(flask.current_app.mongo.get_database()).search(query)

        if len(tokens) != 1:
            flask.abort(403, 'Authorization token is not valid.')

        flask.request.token = auth_token

        return f(*args, **kwargs)
    return wrapper
