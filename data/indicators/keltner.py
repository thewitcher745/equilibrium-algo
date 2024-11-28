import pandas as pd


def keltner(pair_df: pd.DataFrame, window_size=20, atr_period=14, multiplier=2) -> pd.DataFrame:
    """
    Calculate Keltner channels for a DataFrame with OHLC data. The middle Keltner band is a simple moving average. The upper and lower bands are 2
    standard deviations above and below the middle band (by default).

    Args:
    pair_df (pd.DataFrame): DataFrame with 'close' price column
    window_size (int): Period for moving average (default 20)
    atr_period (int):
    multiplier (int): Deviation multiplier (default 2)

    Returns:
        pd.DataFrame: DataFrame with additional columns for Keltner Bands
    """

    # Calculate the moving average (middle band)
    middle_band: pd.Series = pair_df['close'].ewm(span=window_size, adjust=False).mean()

    # Calculate Average True Range
    atr = pair_df['high'] - pair_df['low']
    atr = atr.rolling(window=atr_period).mean()

    # Calculate upper and lower bands
    upper_band: pd.Series = middle_band + (atr * multiplier)
    lower_band: pd.Series = middle_band - (atr * multiplier)

    return pd.DataFrame({
        "middle_keltner_band": middle_band,
        "upper_keltner_band": upper_band,
        "lower_keltner_band": lower_band
    })
