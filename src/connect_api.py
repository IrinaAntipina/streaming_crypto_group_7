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
    raise ValueError("COINMARKET_API saknas i .env!")
if not EXCHANGE_KEY:
    raise ValueError("EXCHANGE_API saknas i .env!")

API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
EXCHANGE_URL = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_KEY}/latest/USD"

def get_exchange():
    try: 
        response = requests.get(EXCHANGE_URL)
        response.raise_for_status()
        return response.json().get("conversion_rates", {})
    except requests.RequestException as e:
        print(f"Fel vid hämtning av växelkurser: {e}")
        return {}

def get_crypto(symbol: str):
  
    symbol_mapping = {
        "TRX": "TRX",
        "S": "S"  
    }
    
    api_symbol = symbol_mapping.get(symbol, symbol)
    
    parameters = {"symbol": api_symbol, "convert": "USD"}
    headers = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": API_KEY}
   
    session = Session()
    session.headers.update(headers)
   
    try:
        response = session.get(API_URL, params=parameters)
        response.raise_for_status()
        data = response.json()["data"][api_symbol]

        price_usd = data["quote"]["USD"]["price"]
        volume_24h = data["quote"]["USD"]["volume_24h"]
        volume_change_24h = data["quote"]["USD"]["volume_change_24h"]
        percent_change_24h = data["quote"]["USD"]["percent_change_24h"]

        return {
            "name": data["name"],
            "symbol": symbol,  
            "price_usd": price_usd,
            "volume_24h": volume_24h,
            "volume_change_24h": volume_change_24h,
            "percent_change_24h": percent_change_24h
        }
       
    except RequestException as e:
        print(f"Fel vid API-anrop: {e}")
        return None

if __name__ == "__main__":
    print("Testing TRX:")
    print(json.dumps(get_crypto("TRX"), indent=4))
    print("\nTesting S:")
    print(json.dumps(get_crypto("S"), indent=4))