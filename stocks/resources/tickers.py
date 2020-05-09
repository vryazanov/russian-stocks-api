"""A set of resources that works with tickers."""
import flask
import flask_restplus
import flask_restplus.fields


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
    'declaration_date': flask_restplus.fields.Date(required=True),
    'amount': flask_restplus.fields.Fixed(required=True),
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

    @ns.marshal_list_with(Payment, envelope='results')
    def get(self):
        """Return list of available tickers."""
        db = flask.current_app.mongo.get_database()
        return list(db.payments.find())

    @ns.expect(Payments, validate=True)
    def post(self):
        """Take a list of payments from request and save to mongo."""
        items = flask.request.json['items']
        db = flask.current_app.mongo.get_database()
        db.payments.insert_many(items)
        return {'success': True}
