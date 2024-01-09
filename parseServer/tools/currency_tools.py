import requests
import os
from cachetools import cached, TTLCache
from loguru import logger

cache = TTLCache(maxsize=1, ttl=60 * 60 * 48)


class CurrencyUpdateError(Exception):
    pass


@cached(cache)
def get_currency_data():
    try:
        data = get_currency_usd_base()
        rates = {}
        for currency, coefficient in data.items():
            rates[currency] = 1 / coefficient
        return rates
    except Exception as e:
        logger.error(f'An error occurred while updating the currency {e}')
        raise CurrencyUpdateError(str(e))


@cached(cache)
def get_currency_usd_base():
    app_id = os.getenv('OPEN_EXCHANGR_RATES_APP_ID')
    base_url = 'https://open.er-api.com/v6/latest'

    params = {'base': 'USD', 'symbols': 'KGS,USD,BYN,AMD,RUB,EUR,KZT'}
    headers = {'Authorization': f'Bearer {app_id}'}

    response = requests.get(base_url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data['rates']
    else:
        raise CurrencyUpdateError(f'responce status code {response.status_code} != 200 \n {response.text}')
