"""A set of resources that works with tickers."""
import flask
import flask_restx
import flask_restx.fields

import stocks.filtersets
import stocks.models
import stocks.repostories
from stocks.namespace import Namespace
from stocks.objects.payment import PaymentModel


ns = Namespace('tickers', description='Tickers related operations')


@ns.route('')
class TickersResource(flask_restx.Resource):
    """Basic resource that works with stock tickers."""

    @ns.doc(params=stocks.filtersets.TickersFilterSet.as_params())
    @ns.marshal_list_with(stocks.models.Ticker, envelope='results')
    def get(self):
        """Return list of available tickers."""
        return stocks.repostories.TickerRepository(
            flask.current_app.mongo.get_database(),
        ).search(
            stocks.filtersets.TickersFilterSet(
                flask.request.args,
            ).query(),
        )


@ns.route('/<ticker>/payments', doc={'params': {
    'ticker': 'code of ticker'}})
class PaymentsResource(flask_restx.Resource):
    """Basic resource that returns data about dividend paymenrs."""

    @ns.doc(params=stocks.filtersets.PaymentsFilterSet.as_params())
    @ns.marshal_entities_list_with(PaymentModel, envelope='results')
    def get(self, ticker):
        """Return list of available tickers."""
        return stocks.repostories.PaymentRepository(
            flask.current_app.mongo.get_database(),
        ).search(
            stocks.filtersets.PaymentsFilterSet(
                flask.request.args,
            ).query().equal_to(ticker=ticker),
        )


@ns.route('/<ticker>/quotes/historical', doc={'params': {
    'ticker': 'code of ticker'}})
class HistoricalQuotesResource(flask_restx.Resource):
    """Basic resource that returns data about dividend paymenrs."""

    @ns.doc(params=stocks.filtersets.QuoteFilterSet.as_params())
    @ns.marshal_list_with(stocks.models.HistoricalQuote, envelope='results')
    def get(self, ticker):
        """Return list of historical stock quotes."""
        return stocks.repostories.QuoteRepository(
            flask.current_app.mongo.get_database(),
        ).search(
            stocks.filtersets.QuoteFilterSet(
                flask.request.args,
            ).query().equal_to(ticker=ticker),
        )
