import pandas as pd


def rsi(pair_df: pd.DataFrame, window_size=14) -> pd.DataFrame:
    """
    Calculate the Relative Strength Index (RSI) for a given pair DataFrame.

    Args:
        pair_df (pd.DataFrame): The dataframe containing the candlesticks for a pair
        window_size(int): The window for calculating the RSI averages. Default is 14.

    Returns:
        pd.DataFrame: A dataframe containing the RSI data, with a single "rsi" column.
    """
    delta = pair_df.close.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss

    return 100 - (100 / (1 + rs)).to_frame(name="rsi")
