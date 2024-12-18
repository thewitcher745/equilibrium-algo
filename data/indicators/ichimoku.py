import pandas as pd


class Ichimoku:
    def __init__(self, pair_df: pd.DataFrame):
        self.pair_df: pd.DataFrame = pair_df
        self.ichimoku_df: pd.DataFrame = pd.DataFrame()

    def tenkan_line(self, window_size: int = 9) -> pd.Series:
        """
        Calculate the Tenka line.
        """
        tenka_highs = self.pair_df.high.rolling(window_size).max()
        tenka_lows = self.pair_df.low.rolling(window_size).min()
        return (tenka_highs + tenka_lows) / 2

    def kijun_line(self, window_size: int = 26) -> pd.Series:
        """
        Calculate the Kijun line.
        """
        return self.tenkan_line(window_size=window_size)

    def lead_span_a(self, shift_size: int = 26) -> pd.Series:
        """
        Calculate the Lead Span A line.
        """
        return ((self.tenkan_line() + self.kijun_line()) / 2).shift(shift_size)

    def lead_span_b(self, window_size: int = 52, shift_size: int = 26) -> pd.Series:
        """
        Calculate the Lead Span B line.
        """
        highest_high = self.pair_df.high.rolling(window_size).max()
        lowest_low = self.pair_df.low.rolling(window_size).min()
        return ((highest_high + lowest_low) / 2).shift(shift_size)

    def lagging_span(self, shift_size: int = 26) -> pd.Series:
        """
        Calculate the Lagging Span.
        """
        return self.pair_df.close.shift(-shift_size)

    def update_ichimoku_df(self, pair_df: pd.DataFrame) -> pd.DataFrame:
        """
        Update the Ichimoku DataFrame with the latest data.
        """
        self.pair_df = pair_df

        lead_span_a_series = self.lead_span_a()
        lead_span_b_series = self.lead_span_b()

        self.ichimoku_df = pd.DataFrame({
            "tenkan": self.tenkan_line(),
            "kijun": self.kijun_line(),
            "lead_span_a": lead_span_a_series,
            "lead_span_b": lead_span_b_series,
            "lagging_span": self.lagging_span(),
            "kumo": lead_span_a_series - lead_span_b_series
        })

        return self.ichimoku_df
