"""A set of resources that are responsible for importing data from crawler."""
import flask
import flask_restx

import stocks.decorators
import stocks.models
import stocks.repostories


ns = flask_restx.Namespace(
    'crawler', description='Import financial data from crawler.')


@ns.route('/tickers', doc={'security': 'Bearer Auth'})
class TickersResource(flask_restx.Resource):
    """Resource to import tickers."""

    method_decorators = (stocks.decorators.auth_required,)

    @ns.doc(id='import_tickers')
    @ns.expect([stocks.models.Ticker], validate=True)
    def post(self):
        """Do tickers importing."""
        stocks.repostories.TickerRepository(
            flask.current_app.mongo.get_database(),
        ).recreate(
            flask.request.json,
        )
        return {'success': True}


@ns.route('/payments', doc={'security': 'Bearer Auth'})
class PaymentsResource(flask_restx.Resource):
    """Resource to import payments."""

    method_decorators = (stocks.decorators.auth_required,)

    @ns.doc(id='import_payments')
    @ns.expect([stocks.models.Payment], validate=True)
    def post(self):
        """Do dividend payment importing."""
        stocks.repostories.PaymentRepository(
            flask.current_app.mongo.get_database(),
        ).recreate(
            flask.request.json,
        )
        return {'success': True}


@ns.route('/quotes/historical', doc={'security': 'Bearer Auth'})
class HistoricalQuotesResource(flask_restx.Resource):
    """Resource to import historical quotes."""

    method_decorators = (stocks.decorators.auth_required,)

    @ns.doc(id='import_quotes')
    @ns.expect([stocks.models.HistoricalQuote], validate=True)
    def post(self):
        """Do historical quotes importing."""
        stocks.repostories.QuoteRepository(
            flask.current_app.mongo.get_database(),
        ).recreate(
            flask.request.json,
        )
        return {'success': True}
