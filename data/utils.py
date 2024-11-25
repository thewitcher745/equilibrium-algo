import time
import aiohttp
import asyncio
import pandas as pd
import datetime
from typing import List, Dict, Tuple


async def fetch_candlestick_data(session: aiohttp.ClientSession, symbol: str, timeframe: str, start_time: int, end_time: int, num_candles: int) -> \
Tuple[str, List[List]]:
    """
    Fetch historical candlestick data for a given trading pair from the Binance API.

    Args:
        session (aiohttp.ClientSession): The aiohttp session to use for the request.
        symbol (str): The trading pair symbol (e.g., 'BTCUSDT').
        timeframe (str): The timeframe of the candles (e.g., '1m', '5m', '1h', '1d').
        start_time (int): The start time in milliseconds since epoch.
        end_time (int): The end time in milliseconds since epoch.
        num_candles (int): The number of candles to fetch.

    Returns:
        tuple: A tuple containing the symbol and the fetched data.
    """
    url = f"https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": timeframe,
        "startTime": start_time,
        "endTime": end_time,
        "limit": num_candles
    }
    async with session.get(url, params=params) as response:
        data = await response.json()
        return symbol, data


async def get_multiple_pairs_data(pairs: List[str], timeframe: str, num_candles: int) -> Dict[str, pd.DataFrame]:
    """
    Fetch historical candlestick data for multiple trading pairs concurrently.

    Args:
        pairs (list): A list of trading pair symbols (e.g., ['BTCUSDT', 'ETHUSDT']).
        timeframe (str): The timeframe of the candles (e.g., '1m', '5m', '1h', '1d').
        num_candles (int): The number of candles to fetch for each pair.

    Returns:
        dict: A dictionary where keys are trading pair symbols and values are pandas DataFrames containing the candlestick data.
    """
    end_time = int(time.time() * 1000)
    timeframe_seconds = pd.Timedelta(timeframe).total_seconds()
    start_time = end_time - (num_candles * int(timeframe_seconds * 1000))

    async with aiohttp.ClientSession(trust_env=True) as session:
        # Create a list of tasks for fetching data for each pair
        tasks = [fetch_candlestick_data(session, pair, timeframe, start_time, end_time, num_candles) for pair in pairs]
        # Run the tasks concurrently
        results = await asyncio.gather(*tasks)

    data_frames = {}
    for symbol, data in results:
        # Convert the data to a pandas DataFrame
        data = [[pd.to_datetime(row[0], unit='ms', utc=True)] + row[1:5] for row in data]
        df = pd.DataFrame(data, columns=["time", "open", "high", "low", "close"])
        # Convert the open, high, low, and close columns to numeric
        df[["open", "high", "low", "close"]] = df[["open", "high", "low", "close"]].apply(pd.to_numeric)
        data_frames[symbol] = df

    return data_frames
