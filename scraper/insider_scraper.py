# scraper/sec_scraper.py

import feedparser
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

# SEC RSS feed for Form 4 filings
RSS_FEED_URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=4&owner=only&count=200"

def scrape_sec_form4(max_filings=50):
    feed = feedparser.parse(RSS_FEED_URL)
    entries = feed.entries[:max_filings]

    data = []

    for entry in entries:
        filing_url = entry.link
        print(f"Processing filing: {filing_url}")
        try:
            res = requests.get(filing_url)
            soup = BeautifulSoup(res.content, "html.parser")
            
            table = soup.find("table", summary="Form 4 Table")

            if not table:
                continue  # No trade table found, skip

            rows = table.find_all("tr")[1:]  # skip header

            for row in rows:
                cols = row.find_all("td")
                if len(cols) < 5:
                    continue

                data.append({
                    "Insider Name": cols[0].text.strip(),
                    "Relationship": cols[1].text.strip(),
                    "Transaction Date": cols[2].text.strip(),
                    "Transaction Code": cols[3].text.strip(),
                    "Shares Traded": cols[4].text.strip(),
                    "Price Per Share": cols[5].text.strip() if len(cols) > 5 else None,
                    "Filing URL": filing_url
                })

            time.sleep(0.5)

        except Exception as e:
            print(f"Error processing {filing_url}: {e}")
            continue

    df = pd.DataFrame(data)

    if not os.path.exists('data'):
        os.makedirs('data')

    df.to_csv("data/sec_insider_trades.csv", index=False)
    print(f" Saved {len(df)} insider trades to data/sec_insider_trades.csv.")

if __name__ == "__main__":
    scrape_sec_form4(max_filings=50)
