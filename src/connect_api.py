import os
import json
import logging
from dotenv import load_dotenv
import requests
from requests import Session, RequestException

load_dotenv()
API_KEY = os.getenv("COINMARKET_API")
EXCHANGE_KEY = os.getenv("EXCHANGE_API")

if not API_KEY:
    raise ValueError("❌ COINMARKET_API saknas i .env!")
if not EXCHANGE_KEY:
    raise ValueError("❌ EXCHANGE_API saknas i .env!")

API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
EXCHANGE_URL = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_KEY}/latest/USD"

def get_exchange():
    try: 
        response = requests.get(EXCHANGE_URL)
        response.raise_for_status()
        return response.json().get("conversion_rates", {})
    except requests.RequestException as e:
        print(f"⚠️ Fel vid hämtning av växelkurser: {e}")
        return {}

def get_crypto(symbol: str):
    parameters = {"symbol": symbol, "convert": "USD"}
    headers = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": API_KEY}
    
    session = Session()
    session.headers.update(headers)
    
    try:
        response = session.get(API_URL, params=parameters)
        response.raise_for_status()
        data = response.json()["data"][symbol]
        
        price_usd = data["quote"]["USD"]["price"]
        
        return {
            "name": data["name"],
            "symbol": data["symbol"],
            "price_usd": price_usd
        }
        
    except RequestException as e:
        print(f"⚠️ Fel vid API-anrop: {e}")
        return None
