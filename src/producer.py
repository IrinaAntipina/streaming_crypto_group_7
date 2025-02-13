import json
import time
import quixstreams as qx
from connect_api import get_crypto, get_exchange

from quixstreams import Application

# Skapa Quix Streams klient
client = qx.Application(broker_adress="broker:29092")
 
# Skapa output-topic för kryptopriser
crypto_topic = client.topic("crypto_prices")
 
# Valutor vi vill konvertera till
SCANDINAVIAN_CURRENCIES = ["SEK", "NOK", "DKK", "EUR"]
 
def fetch_and_stream(symbol="TRX"):
    """ Hämtar kryptodata, konverterar till skandinaviska valutor och skickar till Quix Streams. """
    # Hämta live växelkurser
    exchange_rates = get_exchange()
 
    # Hämta kryptodata i USD
    crypto_data = get_crypto(symbol)
    if not crypto_data:
        print(f"❌ Kunde inte hämta data för {symbol}")
        return
 
    # Konvertera till skandinaviska valutor
    converted_prices = {
        currency: round(crypto_data["price_usd"] * exchange_rates.get(currency, 1), 2)
        for currency in SCANDINAVIAN_CURRENCIES
    }
 
    # Skapa JSON-meddelande för Quix Streams
    message = {
        "name": crypto_data["name"],
        "symbol": crypto_data["symbol"],
        "prices": converted_prices,
        "timestamp": time.time(),
    }
 
    # Skicka data till Quix Streams
    crypto_topic.produce(message)
    print(f"✅ Skickade data till Quix Streams: {message}")
 
# Streama data kontinuerligt
if __name__ == "__main__":
    while True:
        fetch_and_stream("TRX")  # Hämtar TRX-data
        time.sleep(10)  # Väntar 10 sek innan nästa anrop

