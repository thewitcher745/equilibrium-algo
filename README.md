# Equilibrium Trading Signal Generator

This project aims to develop a trading signal generator using the Ichimoku trading indicator and Equilibrium trading strategy principles. The goal is to provide reliable trading signals for various trading pairs.

## Features

- Fetch historical candlestick data from Nobitex and Binance APIs
- Calculate and visualize Ichimoku and RSI trading indicators
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

Run the main script:
    ```
    python main.py
    ```


## Project Structure

- `data/`: Contains utility functions for fetching historical data and cleaning up data.
- `data/indicators/`: Will contain functions for calculating trading indicators (to be implemented).
- `tests/`: Contains unit tests for the project (to be implemented).
