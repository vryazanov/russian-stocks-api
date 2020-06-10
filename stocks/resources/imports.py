"""A set of resources that are responsible for importing data from crawler."""
import flask
import flask_restx

import stocks.decorators
import stocks.repostories
from stocks.objects.payment import PaymentModel
from stocks.objects.quote import QuoteModel
from stocks.objects.ticker import TickerModel


ns = flask_restx.Namespace(
    'crawler', description='Import financial data from crawler.')


class ServiceResource(flask_restx.Resource):
    """Base for resources that require admin authentication."""

    method_decorators = (stocks.decorators.admin_auth_required,)


@ns.route('/tickers', doc={'security': 'Bearer Auth'})
class TickersResource(ServiceResource):
    """Resource to import tickers."""

    @ns.doc(id='import_tickers')
    @ns.expect([TickerModel], validate=True)
    def post(self):
        """Do tickers importing."""
        stocks.repostories.Tickers(
            flask.current_app.mongo.get_database(),
        ).recreate(
            flask.request.json,
        )
        return {'success': True}


@ns.route('/payments', doc={'security': 'Bearer Auth'})
class PaymentsResource(ServiceResource):
    """Resource to import payments."""

    @ns.doc(id='import_payments')
    @ns.expect([PaymentModel], validate=True)
    def post(self):
        """Do dividend payment importing."""
        stocks.repostories.Payments(
            flask.current_app.mongo.get_database(),
        ).recreate(
            flask.request.json,
        )
        return {'success': True}


@ns.route('/quotes/historical', doc={'security': 'Bearer Auth'})
class HistoricalQuotesResource(ServiceResource):
    """Resource to import historical quotes."""

    @ns.doc(id='import_quotes')
    @ns.expect([QuoteModel], validate=True)
    def post(self):
        """Do historical quotes importing."""
        stocks.repostories.Quotes(
            flask.current_app.mongo.get_database(),
        ).recreate(
            flask.request.json,
        )
        return {'success': True}
