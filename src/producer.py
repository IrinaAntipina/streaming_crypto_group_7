from quixstreams import Application
from connect_api import get_crypto, get_exchange
import json
import time
from pprint import pprint

app = Application(broker_address="localhost:9092", consumer_group="coin_group")

messages_topic = app.topic(name="messages", value_serializer="json")

NORDIC_CURRENCY = ["SEK", "NOK", "DKK", "EUR", "ISK"]

def main(symbols=["TRX"]):
    exchange_rates = get_exchange()
    with app.get_producer() as producer:
        while True:
            for symbol in symbols:
                crypto_data = get_crypto(symbol)

                if crypto_data:
                    converted_prices = {
                        currency: round(crypto_data["price_usd"] * exchange_rates.get(currency, 1), 2)
                        for currency in NORDIC_CURRENCY
                    }

                    message = {
                        "name": crypto_data["name"],
                        "symbol": crypto_data["symbol"],
                        "prices": converted_prices,
                        "volume_24h": crypto_data.get("volume_24h", 0), 
                        "volume_change_24h": crypto_data.get("volume_change_24h", 0), 
                        "percent_change_24h": crypto_data.get("percent_change_24h", 0),  
                        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
                    }
                
                    kafka_msg = messages_topic.serialize(key=message["symbol"], value=message)

                    print(f'Producing event: key="{kafka_msg.key}", value="{kafka_msg.value}"')
                    producer.produce(
                        topic=messages_topic.name,
                        key=kafka_msg.key,
                        value=kafka_msg.value,
                    )
            time.sleep(30)

if __name__ == "__main__":
    main(["TRX"])
