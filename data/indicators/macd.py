import pandas as pd


def macd(pair_df: pd.DataFrame, short_window: int = 12, long_window: int = 26, signal_window: int = 9) -> pd.DataFrame:
    """
    Calculate the Moving Average Convergence Divergence (MACD) line and the Signal line.

    Args:
        pair_df (pd.DataFrame): The DataFrame containing the price data.
        short_window (int): The short window for the MACD line.
        long_window (int): The long window for the MACD line.
        signal_window (int): The signal window for the Signal line.

    Returns:
        pd.DataFrame: A DataFrame containing the MACD line and the Signal line.
    """
    short_ema = pair_df["close"].ewm(span=short_window, adjust=False).mean()
    long_ema = pair_df["close"].ewm(span=long_window, adjust=False).mean()

    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()

    return pd.DataFrame({
        "macd_line": macd_line,
        "signal_line": signal_line
    })
