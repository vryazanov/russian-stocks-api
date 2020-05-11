"""A set of object-relational models."""
import flask_restplus


Ticker = flask_restplus.Model('Ticker', {
    'name': flask_restplus.fields.String(
        required=True,
    ),
    'ticker': flask_restplus.fields.String(
        required=True,
        description='code of ticker',
        example='SBER',
    ),
})

Payment = flask_restplus.Model('Payment', {
    'ticker': flask_restplus.fields.String(
        required=True,
        description='code of ticker',
        example='SBER',
    ),
    'declaration_date': flask_restplus.fields.String(
        required=True,
        example='2020-04-01',
    ),
    'amount': flask_restplus.fields.Fixed(
        required=True,
    ),
    'source': flask_restplus.fields.String(
        required=True,
        description='source from which payment was crawled.',
        example='smartlab'
    ),
    'is_forecast': flask_restplus.fields.Boolean(
        required=True,
        description='if true then this payment is a forecast.',
        example=False,
    ),
})

HistoricalQuote = flask_restplus.Model('HistoricalQuote', {
    'ticker': flask_restplus.fields.String(
        required=True,
        description='code of ticker',
        example='SBER',
    ),
    'date': flask_restplus.fields.String(
        required=True,
        description='date of stock quote',
        example='2020-04-01',
    ),
    'open_price': flask_restplus.fields.Fixed(
        required=True,
    ),
    'close_price': flask_restplus.fields.Fixed(
        required=True,
    ),
})
