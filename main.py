import pandas as pd
import asyncio

from data import utils
from data.indicators.bollinger import bollinger
from data.indicators.ichimoku import Ichimoku
from data.indicators.rsi import rsi
from data.indicators.macd import macd
from data.confirmations import Confirmations
from data.indicators.stochastic_osc import stochastic_osc

timeframe = "1m"
# The size of the recent window to check for signal possibilities
recent_window_size = 5

pair_list = pd.read_csv("./pair_list.csv")["pairs"].tolist()

ichimoku = Ichimoku(pd.DataFrame())
confirmations = Confirmations(pd.DataFrame(), pd.DataFrame(), recent_window_size)

while True:
    pairs_data = asyncio.run(utils.get_multiple_pairs_data(pair_list, timeframe, 1000))
    for pair in pair_list:
        try:
            pair_df: pd.DataFrame = pairs_data[pair]

            ichimoku_df = ichimoku.update_ichimoku_df(pair_df)
            rsi_df = rsi(pair_df)
            macd_df = macd(pair_df)
            bollinger_df = bollinger(pair_df)
            stoch_df = stochastic_osc(pair_df)

            # The indicators_df dataframe contains all the indicator data that we need for the analysis.
            indicators_df = pd.concat([ichimoku_df, rsi_df, macd_df, bollinger_df, stoch_df], axis="columns")

            confirmations.update_indicators(indicators_df, pair_df)
            confirmations_dict = confirmations.aggregate_sentiments()

            print(pair)
            print(confirmations_dict)

        except:
            continue
