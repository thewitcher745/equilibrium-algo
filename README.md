# Equilibrium Trading Signal Generator

This project aims to develop a trading signal generator using the Ichimoku trading indicator and Equilibrium trading strategy principles. The goal is to provide reliable trading signals for various trading pairs.

## Features

- Fetch historical candlestick data from Nobitex and Binance APIs
- Calculate and visualize Ichimoku trading indicators
- Implement Equilibrium trading strategy principles
- Generate trading signals based on combined indicators

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/thewitcher745/equilibrium-algo.git
    cd equilibrium-algo
    ```

2. Create a virtual environment:
    ```sh
    python -m virtualenv venv
    ```

3. Activate the virtual environment:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

4. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Fetch historical candlestick data:
    ```python
    from data.utils import get_pair_data

    symbol = 'BTCUSDT'
    timeframe = '1h'
    num_candles = 1000
    candlestick_data = get_pair_data(symbol, timeframe, num_candles)
    print(candlestick_data)
    ```

2. Calculate Ichimoku indicators and generate trading signals (to be implemented).

## Project Structure

- `data/`: Contains utility functions for fetching historical data and cleaning up data.
- `data/indicators/`: Will contain functions for calculating trading indicators (to be implemented).
- `tests/`: Contains unit tests for the project.
