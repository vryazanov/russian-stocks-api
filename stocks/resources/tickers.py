"""A set of resources that works with tickers."""
import flask
import flask_restplus
import flask_restplus.fields

import stocks.query


ns = flask_restplus.Namespace(
    'tickers', description='Tickers related operations')

Ticker = ns.model('Ticker', {
    'name': flask_restplus.fields.String(required=True),
    'ticker': flask_restplus.fields.String(required=True),
})

Tickers = ns.model('Tickers', {
    'items': flask_restplus.fields.List(
        flask_restplus.fields.Nested(Ticker), required=True),
})

Payment = ns.model('Payment', {
    'ticker': flask_restplus.fields.String(required=True),
    'declaration_date': flask_restplus.fields.String(required=True),
    'amount': flask_restplus.fields.Fixed(required=True),
    'source': flask_restplus.fields.String(required=True),
    'is_forecast': flask_restplus.fields.Boolean(required=True),
})

Payments = ns.model('Payments', {
    'items': flask_restplus.fields.List(
        flask_restplus.fields.Nested(Payment), required=True),
})


@ns.route('/tickers')
class TickersResource(flask_restplus.Resource):
    """Basic resource that works with stock tickers."""

    @ns.marshal_list_with(Ticker, envelope='results')
    def get(self):
        """Return list of available tickers."""
        db = flask.current_app.mongo.get_database()
        return list(db.tickers.find())

    @ns.hide
    @ns.expect(Tickers, validate=True)
    def post(self):
        """Take a list of tickers from request and save to mongo."""
        items = flask.request.json['items']
        db = flask.current_app.mongo.get_database()
        db.tickers.insert_many(items)
        return {'success': True}


@ns.route('/payments')
class PaymentsResource(flask_restplus.Resource):
    """Basic resource that returns data about dividend paymenrs."""

    @ns.param('ticker', 'to filter by ticker code')
    @ns.param('is_forecast', 'to filter by forecast flag, `0` or `1`')
    @ns.param('source', 'to filter by source name')
    @ns.marshal_list_with(Payment, envelope='results')
    def get(self):
        """Return list of available tickers."""
        query, db = {}, flask.current_app.mongo.get_database()

        if flask.request.args.get('ticker'):
            ticker = flask.request.args['ticker']
            query['ticker'] = {'$eq': ticker}

        if flask.request.args.get('source'):
            ticker = flask.request.args['source']
            query['source'] = {'$eq': ticker}

        if flask.request.args.get('is_forecast'):
            is_forecast = flask.request.args['is_forecast']
            query['is_forecast'] = {'$eq': stocks.query.to_bool(is_forecast)}

        return list(db.payments.find(query))

    @ns.hide
    @ns.expect(Payments, validate=True)
    def post(self):
        """Take a list of payments from request and save to mongo."""
        items = flask.request.json['items']
        db = flask.current_app.mongo.get_database()
        db.payments.insert_many(items)
        return {'success': True}
