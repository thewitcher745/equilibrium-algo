import pandas as pd


def stochastic_osc(pair_df: pd.DataFrame, window_size=9) -> pd.DataFrame:
    """
    Calculates the stochastic oscillator indicator for pair_df. The %K line is the current close price minus the lowest low, as a percentage of the
    difference between the highest high and the lowest low. The %D line is the 3-period moving average of the %K line.
    Args:
        pair_df: The dataframe containing the candlesticks
        window_size: The min/max calculation window

    Returns:
        pd.DataFrame: Dataframe containing %K and %D data for stochastic oscillator.
    """

    lowest_low: pd.Series = pair_df['low'].rolling(window=window_size).min()
    highest_high: pd.Series = pair_df['high'].rolling(window=window_size).max()

    # %K Line (raw stochastic)
    stoch_k: pd.Series = (pair_df['close'] - lowest_low) / (highest_high - lowest_low) * 100

    # %D Line (3-period moving average of %K)
    stoch_d: pd.Series = stoch_k.rolling(window=3).mean()

    return pd.DataFrame({
        "stoch_k": stoch_k,
        "stoch_d": stoch_d
    })
