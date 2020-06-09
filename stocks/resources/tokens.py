"""Respurces to work with tokens."""
import flask
import flask_restx

from stocks.namespace import Namespace
from stocks.objects.token import Token, TokenModel
from stocks.repostories import Tokens


ns = Namespace('tokens', description='manage user tokens')


@ns.route('/create')
class TokenResource(flask_restx.Resource):
    """Resource to generate token."""

    @ns.doc(id='create')
    @ns.marshal_entity_with(TokenModel)
    def post(self):
        """Generate a new token and return it."""
        token = Token.generate()
        Tokens(flask.current_app.mongo.get_database()).add(token)
        return token
