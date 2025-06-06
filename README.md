# Stevens HFTC Competition – Shifts Strategy (Feb–Apr 2025)

This repository contains the code and methodology used for the **Stevens High-Frequency Trading Competition (HFTC)**, developed between **February and April 2025**. The strategy focuses on automated, risk-managed trading across 30 tickers, leveraging real-time simulations and concurrent order execution.

## Strategy Overview

- ** Price Fluctuation Model**:  
  Simulation data for 30 tickers was used to calculate **percentage-based price fluctuations (p fluc)**, which served as a signal for trade decisions.

- **Buy/Sell Logic**:  
  Orders were placed dynamically based on **scaled `p fluc` values**, determining when a stock was overbought or oversold.

- ** Risk Management**:  
  Exposure per ticker was capped by setting a **maximum share threshold**, ensuring position sizes remained within acceptable risk bounds.

- **Concurrency with `asyncio`**:  
  Leveraged Python’s `asyncio` to process data and place orders across multiple tickers **simultaneously**, reducing latency and improving efficiency.

## Tech Stack

- **Python 3.11+**
- `asyncio` for concurrency
- Data structures for real-time signal processing
- Custom logic for automated trading & position sizing

## Author

Programmed by Indranil Biswas, with research from Harvey Hoang, David Fang, and Yumin Choi as part of the Stevens HFTC Competition (Spring 2025).
