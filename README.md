
# Insider Intel — Tracking Real Insider Trades for Hidden Alpha

**Insider Intel** is a Python-based quant research project built to analyze insider trading activity from SEC Form 4 filings. The goal is to identify patterns in corporate insider behavior that may signal unusually profitable or suspicious trades — a potential source of “hidden alpha.”

This project scrapes live data from [OpenInsider](http://openinsider.com), filters and standardizes it, calculates post-trade returns over multiple time windows, and flags outlier trades. Ultimately, the idea is to assess whether certain insider trades tend to outperform the market and under what conditions.

---

## What It Does

- Scrapes recent insider trades across public U.S. companies from OpenInsider
- Cleans and stores trade data in CSV format
- Pulls historical price data from Yahoo Finance
- Calculates returns after 7 and 14 days from the trade date
- Flags trades that show unusually high post-trade returns for further investigation

## Example: What This Project Does in Simple Terms

Imagine a company executive buys 20,000 shares of their own company at $10 on May 1st, 2025.

Our system does three things:
1. **Tracks that trade** using scraped public filings (e.g., Form 4).
2. **Fetches stock prices** for the following days (e.g., May 8th, May 15th).
3. **Calculates returns** — for example, if the stock hits $12 after 7 days, that’s a 20% gain.

If several such trades by different insiders consistently show 15–30% gains, those trades might contain hidden signals — which is exactly what we're trying to detect.

So in short:  
> We track what insiders are doing, check how their trades perform after a week or two, and try to flag the most “unusually good” ones.


---

## Project Structure

```

insider-intel/
│
├── analysis/
│   ├── profit\_calculator.py      # Calculates % return after insider trade
│   └── suspicion\_scoring.py      # (Optional) Flags trades with unusually high gains
│
├── scraper/
│   ├── historical\_scraper.py     # Scrapes latest trades from OpenInsider
│   └── insider\_scraper.py        # (Future) Fetches deeper insider profiles
│
├── data/
│   ├── historical\_insider\_trades.csv   # Raw trade data from scraping
│   ├── insider\_profits.csv             # Final output with profit calculations
│   └── suspicious\_insider\_trades.csv   # (Optional) Filtered trades of interest
│
├── plots/
│   └── top\_suspicious\_trades.png       # (Optional) Visualized top outliers
│
├── README.md
└── requirements.txt

````

---

## Why This Matters

Insiders — executives, board members, and large shareholders — have access to information most investors don’t. By systematically tracking their trades and overlaying historical performance, this project aims to explore whether any consistent, non-random alpha can be extracted from that behavior.

This project is still a work in progress, and future improvements will include:
- Backtesting strategies based on flagged trades
- Machine learning-based anomaly detection
- Sector-specific signal tuning

---

## Getting Started

Install dependencies:
```bash
pip install -r requirements.txt
````

Run the scraper:

```bash
python scraper/historical_scraper.py
```

Run profit calculator:

```bash
python analysis/profit_calculator.py
```

---

## Author

Built with purpose and persistence by Niraj Patil — MSTM, UIUC.

```

