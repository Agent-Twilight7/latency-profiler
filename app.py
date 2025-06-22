# app.py
from flask import Flask, jsonify
import time
import random

app = Flask(__name__)

@app.route("/market_data")
def market_data():
    time.sleep(random.uniform(0.005, 0.015))  # simulate 5–15ms delay
    return jsonify({"status": "market data sent"})

@app.route("/order_submission")
def order_submission():
    time.sleep(random.uniform(0.020, 0.035))  # simulate 20–35ms delay
    return jsonify({"status": "order submitted"})

@app.route("/trade_ack")
def trade_ack():
    time.sleep(random.uniform(0.010, 0.025))  # simulate 10–25ms delay
    return jsonify({"status": "trade acknowledged"})

if __name__ == '__main__':
    app.run(port=5000)
