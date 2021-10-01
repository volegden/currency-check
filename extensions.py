import json
import requests
import config


class ConvertionException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote, base, amount):
        if quote == base:
            raise ConvertionException(f"Trying to use same currency '{base}'. Please use different currencies. /help")
        try:
            quote_ticker = config.list_of_currencies[quote]
        except KeyError:
            raise ConvertionException(f"Failed to process currency: {quote}.")
        try:
            base_ticker = config.list_of_currencies[base]
        except KeyError:
            raise ConvertionException(f"Failed to process currency: {base}.")
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f"Failed to process amount: {amount}")

        request = requests.get(
            f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}"
        )
        json_load_request = json.loads(request.content)[config.list_of_currencies[base]]

        return json_load_request
