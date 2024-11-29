import pandas as pd
import asyncio
import json
import requests
from datetime import datetime

from data import utils
from data.indicators.keltner import keltner
from data.indicators.ichimoku import Ichimoku
from data.indicators.rsi import rsi
from data.indicators.macd import macd
from data.confirmations import Confirmations
from data.indicators.stochastic_osc import stochastic_osc

# Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = '7755917604:AAETGEYAixKYv5I9GGXSfNH-jltWw47E3rs'
TELEGRAM_CHAT_ID = '-1002442643587'

timeframe = "1h"
recent_window_size = 10
pair_list = pd.read_csv("./pair_list.csv")["pairs"].tolist()

ichimoku = Ichimoku(pd.DataFrame())
confirmations = Confirmations(pd.DataFrame(), pd.DataFrame(), recent_window_size)
previous_signals = {}


def send_telegram_message(message):
    print(message)
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
    }
    response = requests.post(url, json=payload)
    return response


async def fetch_signals():
    global previous_signals
    while True:
        pairs_data = await utils.get_multiple_pairs_data(pair_list, timeframe, 1000)
        current_signals = {}
        for pair in pair_list:
            try:
                pair_df = pairs_data[pair]
                ichimoku_df = ichimoku.update_ichimoku_df(pair_df)
                rsi_df = rsi(pair_df)
                macd_df = macd(pair_df)
                keltner_df = keltner(pair_df)
                stoch_df = stochastic_osc(pair_df)

                indicators_df = pd.concat([ichimoku_df, rsi_df, macd_df, keltner_df, stoch_df], axis="columns")
                confirmations.update_indicators(indicators_df, pair_df)
                confirmations_dict = confirmations.aggregate_sentiments()
                if abs(confirmations_dict["average"]) >= 0.65 and confirmations_dict["confidence"] >= 0.7:
                    current_signals[pair] = confirmations_dict
            except Exception as e:
                continue

        if current_signals.keys() != previous_signals.keys():
            send_telegram_message(
                "---------RECENT SIGNALS---------\n"
            )
            previous_signals = current_signals.copy()
            for pair, signal in current_signals.items():
                message = f"Pair: {pair}\nAverage: {signal['average'] * 100}%\nConfidence: {signal['confidence'] * 100}%\n\nDetails: {json.dumps(signal, indent=4)}"
                send_telegram_message(message)


def run_asyncio_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(fetch_signals())


# Run the asyncio loop in a separate thread
import threading

threading.Thread(target=run_asyncio_loop).start()
