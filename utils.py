import json

import requests
from config import keys

class ConvertionException(Exception):
    pass


class CriptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Валюты не должны быть одинаковыми {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Валюта {quote} не найдена.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Валюта {base} не найдена.')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Неверное значение {amount}.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base
