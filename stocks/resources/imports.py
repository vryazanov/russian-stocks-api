"""A set of resources that are responsible for importing data from crawler."""
import flask_restplus


ns = flask_restplus.Namespace(
    'imports', description='Import financial data from crawler.')


@ns.route('/tickers')
class TickersResource(flask_restplus.Resource):
    """Resource to import tickers."""

    def post(self):
        """Do tickers importing."""
        return {'success': True}


@ns.route('/payments')
class PaymentsResource(flask_restplus.Resource):
    """Resource to import payments."""

    def post(self):
        """Do dividend payment importing."""
        return {'success': True}


@ns.route('/quotes/historical')
class HistoricalQuotesResource(flask_restplus.Resource):
    """Resource to import historical quotes."""

    def post(self):
        """Do historical quotes importing."""
        return {'success': True}
