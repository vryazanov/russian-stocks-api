"""List of method decorators."""
import flask


def auth_required(f):
    """Check authorization token."""
    def wrapper(*args, **kwargs):
        auth_token = flask.request.headers.get('X-Authorization', '')
        if not auth_token:
            flask.abort(401, 'Authorization token is not provided.')
        elif auth_token != flask.current_app.config['AUTH_IMPORT_TOKEN']:
            flask.abort(403, 'Authorization token is not valid.')
        return f(*args, **kwargs)
    return wrapper
