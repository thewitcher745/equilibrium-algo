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

timeframe = "15m"
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


# Indicator Weights
indicator_weights = {
    # Trend Indicators Group (Total Weight: 0.4)
    'ichimoku_group': {
        'total_weight': 0.5,
        'indicators': {
            'ichimoku_cloud_color': 0.3,
            'ichimoku_crossover': 0.5,
            'ichimoku_kumo_relative_position': 0.2
        }
    },

    # Momentum Indicators Group (Total Weight: 0.35)
    'momentum_group': {
        'total_weight': 0.25,
        'indicators': {
            'rsi': 0.5,
            'stochastic_osc': 0.5
        }
    },

    # Volatility Indicators Group (Total Weight: 0.25)
    'volatility_group': {
        'total_weight': 0.25,
        'indicators': {
            'keltner': 1.0  # Only one indicator in this group
        }
    }
}


def calculate_weighted_score(confirmations_dict):
    group_scores = {}

    # Calculate group scores
    for group_name, group_config in indicator_weights.items():
        group_total = 0
        for ind_name, ind_weight in group_config['indicators'].items():
            group_total += confirmations_dict[ind_name] * ind_weight

        # Apply group-level weight
        group_scores[group_name] = group_total * group_config['total_weight']

    # Final score is sum of weighted group scores
    final_score = sum(group_scores.values())

    return final_score, group_scores


def calculate_signal_confidence(confirmations_dict, sign_threshold=0.5):
    # Count indicators agreeing on direction
    total_indicators = len(confirmations_dict)
    bullish_indicators = sum(1 for val in confirmations_dict.values() if val >= sign_threshold)
    bearish_indicators = sum(1 for val in confirmations_dict.values() if val <= -sign_threshold)
    neutral_indicators = total_indicators - bullish_indicators - bearish_indicators

    # Calculate confidence metrics
    confidence_metrics = {
        'bullish_confidence': bullish_indicators / total_indicators,
        'bearish_confidence': bearish_indicators / total_indicators,
        'neutral_percentage': neutral_indicators / total_indicators,

        # Directional agreement score (-1 to 1)
        'directional_consensus': (bullish_indicators - bearish_indicators) / total_indicators
    }

    # Categorize signal strength
    if confidence_metrics['directional_consensus'] > 0.8:
        signal_type = 'Strong Bullish'
    elif confidence_metrics['directional_consensus'] < -0.8:
        signal_type = 'Strong Bearish'
    elif abs(confidence_metrics['directional_consensus']) > 0.3:
        signal_type = 'Moderate ' + ('Bullish' if confidence_metrics['directional_consensus'] > 0 else 'Bearish')
    else:
        signal_type = 'Neutral'

    confidence_metrics['signal_type'] = signal_type

    return confidence_metrics


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

                score = calculate_weighted_score(confirmations_dict)
                confidence = calculate_signal_confidence(confirmations_dict)
                confirmations_dict["average"] = score
                confirmations_dict["confidence"] = confidence

                if confidence["signal_type"] == "Strong Bullish" or confidence["signal_type"] == "Strong Bearish":
                    current_signals[pair] = confirmations_dict
            except Exception as e:
                print(e)
                continue

        if current_signals.keys() != previous_signals.keys():
            send_telegram_message(
                "---------RECENT SIGNALS---------\n"
            )
            previous_signals = current_signals.copy()
            for pair, signal in current_signals.items():
                message = f"Pair: {pair}\nAverage: {signal['average'][0]}\nConfidence: {signal['confidence']["signal_type"]}\n\nDetails: {json.dumps(signal, indent=4)}"
                print(message)
                send_telegram_message(message)


def run_asyncio_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(fetch_signals())


# Run the asyncio loop in a separate thread
import threading

threading.Thread(target=run_asyncio_loop).start()
