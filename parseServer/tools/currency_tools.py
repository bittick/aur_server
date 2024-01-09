import requests
import os
from cachetools import cached, TTLCache
from loguru import logger

cache = TTLCache(maxsize=1, ttl=60 * 60 * 48)


class CurrencyUpdateError(Exception):
    pass


@cached(cache)
def get_currency_data():
    app_id = '5b4d85b700c04275a5314faa95c73dd0'
    base_url = 'https://open.er-api.com/v6/latest'

    params = {'base': 'USD', 'symbols': 'KGS,USD,BYN,AMD,RUB,EUR,KZT'}
    headers = {'Authorization': f'Bearer {app_id}'}

    response = requests.get(base_url, params=params, headers=headers)
    try:
        if response.status_code == 200:
            data = response.json()
            rates = {}
            for currency, coefficient in data['rates'].items():
                rates[currency] = 1 / coefficient
            return rates
    except Exception as e:
        logger.error(f'An error occurred while updating the currency {e}')
        raise CurrencyUpdateError(str(e))
