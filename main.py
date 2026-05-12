import requests
import sqlite3
import os
from datetime import datetime
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("COINGECKO_API_KEY")

# Tokens we want to track
COINS = ["bitcoin", "ethereum", "chainlink", "solana"]

def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": ",".join(COINS),
        "order": "market_cap_desc",
        "sparkline": False,
        "x_cg_demo_api_key": API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()

def save_to_database(data):
    conn = sqlite3.connect("crypto.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id TEXT,
            name TEXT,
            symbol TEXT,
            current_price REAL,
            market_cap REAL,
            total_volume REAL,
            price_change_24h REAL,
            timestamp TEXT
        )
    """)

    for coin in data:
        cursor.execute("""
            INSERT INTO prices VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            coin["id"],
            coin["name"],
            coin["symbol"],
            coin["current_price"],
            coin["market_cap"],
            coin["total_volume"],
            coin["price_change_percentage_24h"],
            datetime.now().isoformat()
        ))

    conn.commit()
    conn.close()
    print(f"Saved data for {len(data)} coins at {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    print("Fetching crypto data...")
    data = fetch_crypto_data()
    save_to_database(data)
    print("Done!")
    