"""Resources to work with investment portfolios."""
import flask
import flask_restx

from stocks.decorators import auth_required
from stocks.filters.query import Query
from stocks.namespace import Namespace
from stocks.objects.asset import Asset, AssetModel
from stocks.repostories import Assets


ns = Namespace('portfolio', description='Portfolio related operations')


@ns.route('/assets', doc={'security': 'Bearer Auth'})
class AssetResource(flask_restx.Resource):
    """List of user's assets."""

    method_decorators = (auth_required,)

    @ns.marshal_entities_list_with(AssetModel, envelope='results')
    def get(self):
        """Return list of user's assets."""
        return Assets(
            flask.current_app.mongo.get_database(),
        ).search(
            Query().equal_to(owner=flask.request.token),
        )

    @ns.expect(AssetModel, validate=True)
    @ns.marshal_entity_with(AssetModel)
    def post(self):
        """Create an asset."""
        asset = Asset(
            owner=flask.request.token,
            ticker=flask.request.json['ticker'],
            quantity=flask.request.json['quantity'],
        )
        Assets(flask.current_app.mongo.get_database()).add(asset)
        return asset

    def delete(self):
        """Drop all assets."""
        return Assets(
            flask.current_app.get_database(),
        ).drop(
            Query().equal_to(owner=flask.request.token),
        )
