import pandas as pd
import asyncio

from data import utils
from data.indicators.ichimoku import Ichimoku
from data.indicators.rsi import rsi

timeframe = "1h"
# The size of the recent window to check for signal possibilities
recent_window_size = 5

pair_list = pd.read_csv("./pair_list.csv")["pairs"].tolist()

ichimoku = Ichimoku(pd.DataFrame())

while True:
    pairs_data = asyncio.run(utils.get_multiple_pairs_data(pair_list, timeframe, 1000))
    for pair in pair_list:
        pair_df: pd.DataFrame = pairs_data[pair]
        ichimoku_df = ichimoku.update_ichimoku_df(pair_df)
        rsi_df = rsi(pair_df)

        # The indicators_df dataframe contains all the indicator data that we need for the analysis.
        indicators_df = pd.concat([ichimoku_df, rsi_df], axis="columns")

    break
