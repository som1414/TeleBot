import requests
import json
from config import keys


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(original: str, result: str, quantity: str):

        if original == result:
            raise APIException('Невозможно перевести валюту саму в себя')

        try:
            original_ticker = keys[original]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {original}')

        try:
            result_ticker = keys[result]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {result}')

        try:
            quantity = float(quantity)
        except ValueError:
            raise APIException(f'Не удалось обработать колличество валюты {quantity}')

        r = requests.get(
            f'https://free.currconv.com/api/v7/convert?q={original_ticker}_{result_ticker}&compact=ultra&apiKey=609590f5ef6ff491184c')
        coast = json.loads(r.content)[f'{keys[original]}_{keys[result]}'] * quantity

        return coast
