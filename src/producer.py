from quixstreams import Application
from connect_api import get_crypto, get_exchange
import json
import time
from pprint import pprint

app = Application(broker_address="localhost:9092", consumer_group="coin_group")

messages_topic = app.topic(name="messages", value_serializer="json")

SCANDINAVIAN_CURRENCIES = ["SEK", "NOK", "DKK", "EUR"]

def main(symbol="TRX"):
    exchange_rates = get_exchange()
    crypto_data = get_crypto(symbol)
    
    converted_prices = {
        currency: round(crypto_data["price_usd"] * exchange_rates.get(currency, 1), 2)
        for currency in SCANDINAVIAN_CURRENCIES
    }
   
    message = {
        "name": crypto_data["name"],
        "symbol": crypto_data["symbol"],
        "prices": converted_prices,
        "timestamp": time.time(),
    }

    pprint(message)

if __name__ == "__main__":
    while True:
        main("TRX")  
        time.sleep(30)

