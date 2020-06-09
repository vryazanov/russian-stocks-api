"""Resources to work with investment portfolios."""
import flask_restx

from stocks.decorators import auth_required
from stocks.namespace import Namespace


ns = Namespace('portfolio', description='Portfolio related operations')


@ns.route('', doc={'security': 'Bearer Auth'})
class PortfolioResource(flask_restx.Resource):
    """Reosurce that can create or delete user's portfolio."""

    method_decorators = (auth_required,)

    def get(self):
        """Return portfolio."""
        return {'success': True}


@ns.route('/assets', doc={'security': 'Bearer Auth'})
class AssetResource(flask_restx.Resource):
    """List of user's assets."""

    def get(self):
        """Return list of assets."""
        return {'success': True}
