from flask import Flask, render_template, jsonify
import requests
import redis


app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)


@app.route("/")
def home_page():
    # Increment the visit count in Redis
    r.incr("visit_count")
    visit_count = r.get("visit_count").decode()  # Retrieve the visit count from Redis
    return render_template("HomePage.html", visit_count=visit_count)


@app.route("/eth")
def eth():
    eth_price = r.get("eth_price")
    if eth_price is None:
        # Make a GET request to the CoinDesk API
        eth_response = requests.get("https://api.coinstats.app/public/v1/coins/ethereum")

        # Extract the Ethereum price from the API response
        if eth_response.status_code == 200:
            eth_price = eth_response.json()["coin"]["price"]
            # Store the Ethereum price in Redis for future use
            r.set("eth_price", eth_price)
            # Set the expiration time for the key (e.g., 1 hour)
            r.expire("eth_price", 3600)
    else:
        eth_price = eth_price.decode()  # Convert bytes to string
    
    # Pass the Ethereum price data to the template
    return render_template("eth.html", eth_price=eth_price)


@app.route("/btc")
def btc():
    bitcoin_price = r.get("bitcoin_price")
    if bitcoin_price is None:
        # Make a GET request to the CoinDesk API
        btc_response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
    
        # Extract the Bitcoin price from the API response
        if btc_response.status_code == 200:
            bitcoin_price = btc_response.json()["bpi"]["USD"]["rate"]
            # Store the Bitcoin price in Redis for future use
            r.set("bitcoin_price", bitcoin_price)
            # Set the expiration time for the key (e.g., 1 hour)
            r.expire("bitcoin_price", 3600)
    else:
        bitcoin_price = bitcoin_price.decode()  # Convert bytes to string
 
    # Pass the Bitcoin price data to the template
    return render_template("btc.html", bitcoin_price
