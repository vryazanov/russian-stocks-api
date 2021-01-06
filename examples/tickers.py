"""Get available tickers from the API."""
import bravado.client
import bravado.requests_client


URL = 'https://russian-stocks-api.herokuapp.com/swagger.json'


api = bravado.client.SwaggerClient.from_url(URL)
print(dir(api.tickers))
