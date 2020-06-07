"""A set of object-relational models."""
import flask_restx


Ticker = flask_restx.Model('Ticker', {
    'name': flask_restx.fields.String(
        required=True,
        example='Sberbank',
    ),
    'ticker': flask_restx.fields.String(
        required=True,
        description='code of ticker',
        example='SBER',
    ),
})

Payment = flask_restx.Model('Payment', {
    'ticker': flask_restx.fields.String(
        required=True,
        description='code of ticker',
        example='SBER',
    ),
    'declaration_date': flask_restx.fields.String(
        required=True,
        example='2020-04-01',
    ),
    'amount': flask_restx.fields.Fixed(
        required=True,
    ),
    'source': flask_restx.fields.String(
        required=True,
        description='source from which payment was crawled.',
        example='smartlab',
    ),
    'is_forecast': flask_restx.fields.Boolean(
        required=True,
        description='if true then this payment is a forecast.',
        example=False,
    ),
})

HistoricalQuote = flask_restx.Model('HistoricalQuote', {
    'ticker': flask_restx.fields.String(
        required=True,
        description='code of ticker',
        example='SBER',
    ),
    'date': flask_restx.fields.String(
        required=True,
        description='date of stock quote',
        example='2020-04-01',
    ),
    'open_price': flask_restx.fields.Fixed(
        required=True,
    ),
    'close_price': flask_restx.fields.Fixed(
        required=True,
    ),
})
