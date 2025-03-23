# app.py
from flask import Flask, request, jsonify, send_file
import requests
from datetime import datetime

app = Flask(__name__)

# Function to fetch crypto price from CryptoCompare API
def get_crypto_price(crypto_symbol):
    url = f"https://min-api.cryptocompare.com/data/price?fsym={crypto_symbol}&tsyms=USD"
    try:
        response = requests.get(url)
        if response.status_code == 200 and "USD" in response.json():
            return response.json()["USD"]
        return None
    except requests.exceptions.RequestException:
        return None

crypto_map = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "litecoin": "LTC",
    "ripple": "XRP",
    "dogecoin": "DOGE",
    "cardano": "ADA",
    "polkadot": "DOT",
    "binancecoin": "BNB",
    "solana": "SOL",
    "chainlink": "LINK"
}

@app.route('/price', methods=['GET'])
def fetch_price():
    crypto_name = request.args.get('crypto', '').lower().strip()
    crypto_symbol = crypto_map.get(crypto_name)
    if not crypto_symbol:
        return jsonify({"error": f"Cryptocurrency '{crypto_name}' not found"}), 400
    price = get_crypto_price(crypto_symbol)
    if price:
        return jsonify({"name": crypto_name.capitalize(), "price": price, "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")})
    return jsonify({"error": f"Could not fetch price"}), 500

@app.route('/')
def index():
    return send_file('index.html')  # Serve index.html from root directory

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)