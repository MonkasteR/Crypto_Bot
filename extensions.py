import json

import requests

from config import keys, API_KEY


class ConvertionException(Exception):
    pass


class CriptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Валюты не должны быть одинаковыми {base}.')

        try:
            quote_ticker = keys[quote.lower()]
        except KeyError:
            raise ConvertionException(f'Валюта {quote} не найдена.')

        try:
            base_ticker = keys[base.lower()]
        except KeyError:
            raise ConvertionException(f'Валюта {base} не найдена.')

        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise ConvertionException(f'Неверное значение {amount}.')

        r = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}&api_key={API_KEY}')
        result = json.loads(r.content)[keys[base]] * amount

        return result
