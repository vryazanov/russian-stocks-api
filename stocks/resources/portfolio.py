"""Resources to work with investment portfolios."""
import flask
import flask_restx

from stocks.containers import Repositories
from stocks.decorators import auth_required
from stocks.filters.query import AssetQuery
from stocks.namespace import Namespace
from stocks.objects.asset import Asset, AssetModel
from stocks.objects.portfolio import Portfolio, PortfolioModel


ns = Namespace('portfolio', description='Portfolio related operations')


@ns.route('', doc={'security': 'Bearer Auth'})
class PortfolioResource(flask_restx.Resource):
    """Portfolio resource."""

    method_decorators = (auth_required,)

    @ns.doc(id='get_portfolio')
    @ns.marshal_entity_with(PortfolioModel)
    def get(self):
        """Return info about user's portfolio."""
        return Portfolio(flask.request.token, Repositories.assets)


@ns.route('/assets', doc={'security': 'Bearer Auth'})
class AssetResource(flask_restx.Resource):
    """List of user's assets."""

    method_decorators = (auth_required,)

    @ns.doc(id='get_assets')
    @ns.marshal_entities_list_with(AssetModel, envelope='results')
    def get(self):
        """Return list of user's assets."""
        query = AssetQuery().belong_to(flask.request.token)
        return Repositories.assets.search(query)

    @ns.doc(id='post_asset')
    @ns.expect(AssetModel, validate=True)
    @ns.marshal_entity_with(AssetModel)
    def post(self):
        """Create an asset."""
        asset = Asset(
            owner=flask.request.token,
            ticker=flask.request.json['ticker'],
            quantity=flask.request.json['quantity'],
            payments=Repositories.payments,
        )
        Repositories.assets.add(asset)
        return asset

    @ns.doc(id='drop_assets')
    def delete(self):
        """Drop all assets."""
        query = AssetQuery().belong_to(owner=flask.request.token)
        return Repositories.assets.drop(query)
