"""A set of resources that works with tickers."""
import flask
import flask_restplus
import flask_restplus.fields


ns = flask_restplus.Namespace(
    'tickers', description='Tickers related operations')

Ticker = ns.model('Ticker', {
    'name': flask_restplus.fields.String(required=True),
    'name_verbose': flask_restplus.fields.String(required=True),
})

Tickers = ns.model('Tickers', {
    'items': flask_restplus.fields.List(
        flask_restplus.fields.Nested(Ticker), required=True),
})


@ns.route('/tickers')
class TickersResource(flask_restplus.Resource):
    """Basic resource that works with stock tickers."""

    @ns.marshal_list_with(Ticker, envelope='results')
    def get(self):
        """Return list of available tickers."""
        return list(flask.current_app.mongo.db.tickers.find())

    @ns.expect(Tickers, validate=True)
    def post(self):
        """Take a list of tickers from request and save to mongo."""
        items = flask.request.json['items']
        flask.current_app.mongo.db.tickers.insert_many(items)
        return {'success': True}
