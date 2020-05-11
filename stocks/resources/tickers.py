"""A set of resources that works with tickers."""
import flask
import flask_restplus
import flask_restplus.fields

import stocks.filtersets
import stocks.models


ns = flask_restplus.Namespace(
    'tickers', description='Tickers related operations')


@ns.route('')
class TickersResource(flask_restplus.Resource):
    """Basic resource that works with stock tickers."""

    @ns.doc(params=stocks.filtersets.TickersFilterSet.as_params())
    @ns.marshal_list_with(stocks.models.Ticker, envelope='results')
    def get(self):
        """Return list of available tickers."""
        filter_set = stocks.filtersets.TickersFilterSet(flask.request.args)
        db = flask.current_app.mongo.get_database()
        return list(db.tickers.find(filter_set.query()))


@ns.route('/<ticker>/payments', doc={'params': {
    'ticker': stocks.models.Payment['ticker'].description}})
class PaymentsResource(flask_restplus.Resource):
    """Basic resource that returns data about dividend paymenrs."""

    @ns.doc(params=stocks.filtersets.PaymentsFilterSet.as_params())
    @ns.marshal_list_with(stocks.models.Payment, envelope='results')
    def get(self, ticker):
        """Return list of available tickers."""
        filter_set = stocks.filtersets.PaymentsFilterSet(flask.request.args)
        query = filter_set.query().equal_to(ticker=ticker)

        db = flask.current_app.mongo.get_database()
        return list(db.payments.find(query))


@ns.route('/<ticker>/quotes/historical', doc={'params': {
    'ticker': stocks.models.Payment['ticker'].description}})
class HistoricalQuotesResource(flask_restplus.Resource):
    """Basic resource that returns data about dividend paymenrs."""

    @ns.doc(params=stocks.filtersets.QuoteFilterSet.as_params())
    @ns.marshal_list_with(stocks.models.HistoricalQuote, envelope='results')
    def get(self, ticker):
        """Return list of historical stock quotes."""
        filter_set = stocks.filtersets.QuoteFilterSet(flask.request.args)
        query = filter_set.query().equal_to(ticker=ticker)

        db = flask.current_app.mongo.get_database()
        return list(db.quotes.find(query))
