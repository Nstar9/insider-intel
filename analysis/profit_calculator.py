import pandas as pd
import yfinance as yf
import numpy as np
from datetime import datetime, timedelta
import time
import os

INPUT_CSV = 'data/historical_insider_trades.csv'
OUTPUT_CSV = 'data/insider_profits.csv'
DAYS_TO_CHECK = [7, 14]

def fetch_price_data(tickers, start_date, end_date, batch_size=5):
    all_data = {}
    tickers = list(set(tickers))

    for i in range(0, len(tickers), batch_size):
        batch = tickers[i:i + batch_size]
        print(f"[INFO] Downloading batch {i // batch_size + 1}: {batch}")
        for attempt in range(3):
            try:
                data = yf.download(
                    tickers=batch,
                    start=start_date,
                    end=end_date,
                    group_by="ticker",
                    progress=False,
                    auto_adjust=True,
                    threads=True
                )
                if not data.empty:
                    if isinstance(data.columns, pd.MultiIndex):
                        for symbol in batch:
                            if symbol in data.columns.levels[0]:
                                all_data[symbol] = data[symbol]
                    else:
                        all_data[batch[0]] = data
                    break
                else:
                    print(f"[WARN] Empty data for batch {batch}, attempt {attempt+1}")
            except Exception as e:
                print(f"[ERROR] Failed batch {batch}, attempt {attempt+1}: {e}")
            time.sleep(10 * (attempt + 1))
        time.sleep(10)

    if not all_data:
        return pd.DataFrame()

    combined = pd.concat(all_data, axis=1)
    return combined

def calculate_profits(df, price_data, days_after):
    profit_col = f"Profit_After_{days_after}_Days"
    df[profit_col] = np.nan

    for idx, row in df.iterrows():
        ticker = row['Ticker']
        trade_date = row['Trade Date']

        try:
            if ticker not in price_data.columns.levels[0]:
                continue

            price_series = price_data[ticker]['Close']
            price_series = price_series[price_series.index >= pd.to_datetime(trade_date)]
            if len(price_series) > days_after:
                start_price = price_series.iloc[0]
                end_price = price_series.iloc[days_after]
                df.at[idx, profit_col] = round(((end_price - start_price) / start_price) * 100, 2)
        except Exception as e:
            print(f"[ERROR] Calculating profit for {ticker}: {e}")

def main():
    if not os.path.exists(INPUT_CSV):
        print(f"Input file {INPUT_CSV} not found.")
        return

    df = pd.read_csv(INPUT_CSV, parse_dates=["Trade Date"])
    df['Ticker'] = df['Ticker'].str.strip().str.upper().str.replace('.', '-', regex=False)

    unique_tickers = df['Ticker'].unique().tolist()
    print(f"[INFO] Fetching price data for {len(unique_tickers)} tickers")

    start_date = df['Trade Date'].min() - timedelta(days=2)
    end_date = datetime.today()
    price_data = fetch_price_data(unique_tickers, start_date, end_date)

    if price_data.empty:
        print("[ERROR] No price data fetched")
        return

    for days in DAYS_TO_CHECK:
        calculate_profits(df, price_data, days)

    df.to_csv(OUTPUT_CSV, index=False)
    print(f"[DONE] Saved {len(df)} records with profit data to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
