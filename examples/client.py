"""Simple API client."""
import urllib.parse

import bravado.client
import bravado.requests_client


URL = 'https://russian-stocks-api.herokuapp.com/swagger.json'
DOMAIN = urllib.parse.urlparse(URL).netloc

ASSETS = (
    ('YNDX', 94),
    ('GAZP', 960),
    ('LKOH', 91),
    ('SBERP', 2950),
    ('FEES', 400000),
    ('GMNK', 17),
    ('LSNGP', 1300),
    ('PHOR', 46),
    ('MAGN', 2100),
    ('SBER', 250),
)

api = bravado.client.SwaggerClient.from_url(URL)
token = api.tokens.create().response()

print('Your secret key:', token.result.secret_key)

options = {
    'headers': {
        'x-authorization': token.result.secret_key,
    },
}

for ticker, quantity in ASSETS:
    api.portfolio.post_asset(
        payload={
            'ticker': ticker,
            'quantity': quantity,
        },
        _request_options=options,
    ).response()

portfolio = api.portfolio.get_portfolio(_request_options=options).response()

for payment in portfolio.result.payments:
    print('Year: {0}. Amount: {1}'.format(payment.year, payment.amount))
