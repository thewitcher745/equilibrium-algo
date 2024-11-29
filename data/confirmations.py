"""
This file will contain different confirmation checks for the signals. The confirmation class will have a method for each confirmation check. The
methods will take the indicators_df dataframe as input and return a boolean value indicating whether the confirmation check is met or not. At the end,
all the confirmation checks will be aggregated using an AND operation to generate the final signal.
"""
import inspect

import pandas as pd
import numpy as np


class Confirmations:
    def __init__(self, indicators_df: pd.DataFrame, pair_df: pd.DataFrame, recent_window_size: int):
        self.indicators_df = indicators_df
        self.pair_df = pair_df
        self.recent_window_size = recent_window_size

    def update_indicators(self, indicators_df: pd.DataFrame, pair_df: pd.DataFrame):
        self.indicators_df = indicators_df
        self.pair_df = pair_df

    def aggregate_sentiments(self) -> dict:
        """
        This method aggregates all the confirmations and summarizes them into a pandas DataFrame with a column containing the final signal. The other
        columns wil contain the results of the individual checks.

        Returns:
            dict: A Pandas dataframe with a single row containing the confirmation data
        """
        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        total_sum = 0
        total_weight = 0

        confirmations_dict = dict()

        for name, method in methods:
            if not name.startswith('__') and name != 'update_indicators' and name != 'aggregate_sentiments':
                confirmation_value = round(method(), 2)

                # If the confirmation value is small, give it half the weight
                weight = 1
                if -0.1 < confirmation_value < 0.1:
                    weight = 0.5

                total_sum += confirmation_value
                total_weight += weight

                confirmations_dict[name] = confirmation_value

        confirmations_dict["average"] = round(float(total_sum / total_weight), 2)
        confirmations_dict["confidence"] = round(float(1 - np.var(list(confirmations_dict.values()))), 2)

        return confirmations_dict

    def ichimoku_crossover(self) -> int:
        """
        Check if the Tenkan-sen line crosses above the Kijun-sen line. This is checked by seeing if the lines cross over in a window of size
        recent_window_size. The check for the crossing is done by comparing the value of the difference between the Tenkan-sen line and the Kijun-sen
        line, and finding the sign change in the difference.
        """

        tenkan_sen = self.indicators_df["tenkan"]
        kijun_sen = self.indicators_df["kijun"]

        tenkan_sen_diff = tenkan_sen - kijun_sen

        # Check if a sign change has happened in the recent window
        # If the tenkan line went from below the kijun line to above it, return "BUY". If the tenkan line went from above the kijun line to below it,
        # return "SELL"

        if tenkan_sen_diff[-self.recent_window_size:].iloc[0] > 0 > tenkan_sen_diff[-self.recent_window_size:].iloc[-1]:
            return -1
        elif tenkan_sen_diff[-self.recent_window_size:].iloc[0] < 0 < tenkan_sen_diff[-self.recent_window_size:].iloc[-1]:
            return 1
        else:
            return 0

    def ichimoku_kumo_relative_position(self) -> int:
        """
        If the last close price is above both lead span A and B, it's a RISING signal. Otherwise, it's a FALLING signal.
        """
        last_close = self.pair_df.close.iloc[-1]
        lead_span_a = self.indicators_df["lead_span_a"].iloc[-1]
        lead_span_b = self.indicators_df["lead_span_b"].iloc[-1]

        if last_close > max(lead_span_b, lead_span_a):
            return 1

        elif last_close < min(lead_span_b, lead_span_a):
            return -1

        else:
            return 0

    def ichimoku_cloud_color(self):
        """
        If the lead span A is above the lead span B, it's a RISING signal. If the lead span A is below the lead span B, it's a FALLING signal.
        """
        lead_span_a = self.indicators_df["lead_span_a"].iloc[-1]
        lead_span_b = self.indicators_df["lead_span_b"].iloc[-1]

        if lead_span_a > lead_span_b:
            return 1

        elif lead_span_a < lead_span_b:
            return -1

        else:
            return 0

    def rsi(self) -> float:
        """
        Return a float value for the RSI.
        """

        rsi = self.indicators_df["rsi"].iloc[-1]

        return float((50 - rsi) / 100)

    # def macd(self) -> int:
    #     """
    #     MACD-based confirmation. If the MACD line crosses above the Signal line, it's a RISING signal, or an output of 1. If the MACD line crosses
    #     below the Signal line, it's a FALLING signal or an output of -1. Otherwise, it's an output of 0, indicating no clear signal.
    #     """
    #
    #     # If in the recent window a crossing of MACD and signal lines has occurred, return 1 for a buy signal, -1 for a sell signal, and 0 for no
    #     # signal.
    #
    #     macd_line: pd.Series = self.indicators_df["macd_line"]
    #     signal_line: pd.Series = self.indicators_df["signal_line"]
    #
    #     # Calculate the difference between MACD line and Signal line
    #     macd_diff = macd_line - signal_line
    #
    #     # Check for crossing in the recent window
    #     if macd_diff[-self.recent_window_size:].iloc[0] < 0 < macd_diff[-self.recent_window_size:].iloc[-1]:
    #         return 1
    #     elif macd_diff[-self.recent_window_size:].iloc[0] > 0 > macd_diff[-self.recent_window_size:].iloc[-1]:
    #         return -1
    #     else:
    #         return 0

    def keltner(self):
        """
        Generate confirmation signal based on Bollinger Bands
        """
        last_candle = self.pair_df.iloc[-1]
        keltner_band_values = self.indicators_df.iloc[-1]

        if last_candle.high > keltner_band_values['upper_keltner_band']:
            return -1  # Potentially overbought
        elif last_candle.low < keltner_band_values['lower_keltner_band']:
            return 1  # Potentially oversold
        elif last_candle.high > keltner_band_values['middle_keltner_band']:
            return +0.5  # Mild bullish
        elif last_candle.low < keltner_band_values['middle_keltner_band']:
            return 0.5  # Mild bearish
        else:
            return 0  # Neutral

    def stochastic_osc(self) -> float:
        last_indicator = self.indicators_df.iloc[-1]

        if last_indicator['stoch_k'] > 80:
            return -1  # Overbought
        elif last_indicator['stoch_k'] < 20:
            return 1  # Oversold

        elif last_indicator['stoch_k'] > last_indicator['stoch_d']:
            return 0.5  # Bullish momentum
        else:
            return -0.5  # Bearish momentum
