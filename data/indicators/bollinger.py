import pandas as pd


def bollinger(pair_df: pd.DataFrame, window=20, std_multiplier=2) -> pd.DataFrame:
    """
    Calculate Bollinger Bands for a DataFrame with OHLC data. The middle bollinger band is a simple moving average. The upper and lower bands are 2
    standard deviations above and below the middle band (by default).

    Args:
    pair_df: DataFrame with 'close' price column
    window: Period for moving average (default 20)
    std_multiplier: Standard deviation multiplier (default 2)

    Returns:
        pd.DataFrame: DataFrame with additional columns for Bollinger Bands
    """

    # Calculate the moving average (middle band)
    middle_band: pd.Series = pair_df['close'].rolling(window=window).mean()

    # Calculate standard deviation
    std_dev: pd.Series = pair_df['close'].rolling(window=window).std()

    # Calculate upper and lower bands
    upper_band: pd.Series = middle_band + (std_dev * std_multiplier)
    lower_band: pd.Series = middle_band - (std_dev * std_multiplier)

    return pd.DataFrame({
        "middle_bollinger_band": middle_band,
        "upper_bollinger_band": upper_band,
        "lower_bollinger_band": lower_band
    })
