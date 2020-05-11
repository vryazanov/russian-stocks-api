"""A set of resources that are responsible for importing data from crawler."""
import flask_restplus

import stocks.decorators


ns = flask_restplus.Namespace(
    'imports', description='Import financial data from crawler.')


@ns.route('/tickers', doc={'security': 'Bearer Auth'})
class TickersResource(flask_restplus.Resource):
    """Resource to import tickers."""

    method_decorators = (stocks.decorators.auth_required,)

    def post(self):
        """Do tickers importing."""
        return {'success': True}


@ns.route('/payments', doc={'security': 'Bearer Auth'})
class PaymentsResource(flask_restplus.Resource):
    """Resource to import payments."""

    method_decorators = (stocks.decorators.auth_required,)

    def post(self):
        """Do dividend payment importing."""
        return {'success': True}


@ns.route('/quotes/historical', doc={'security': [{'Bearer Auth': 'test'}]})
class HistoricalQuotesResource(flask_restplus.Resource):
    """Resource to import historical quotes."""

    method_decorators = (stocks.decorators.auth_required,)

    def post(self):
        """Do historical quotes importing."""
        return {'success': True}
