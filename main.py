import pandas as pd
import asyncio

from data import utils
from data.indicators.ichimoku import Ichimoku

timeframe = "1h"
# The size of the recent window to check for signal possibilities
recent_window_size = 5

pair_list = pd.read_csv("./pair_list.csv")["pairs"].tolist()

ichimoku = Ichimoku(pd.DataFrame())

while True:
    pairs_data = asyncio.run(utils.get_multiple_pairs_data(pair_list, timeframe, 1000))
    for pair in pair_list:
        pair_df: pd.DataFrame = pairs_data[pair]
        ichimoku.update_ichimoku_df(pair_df)

    break
