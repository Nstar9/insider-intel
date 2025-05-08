import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from datetime import datetime

def scrape_historical_insiders(pages=100):
    base_url = "http://openinsider.com/latest-insider-trading/"
    all_data = []

    for page in range(1, pages + 1):
        url = f"{base_url}{page}"
        print(f"Scraping Page {page}: {url}")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            table = soup.find("table", class_="tinytable")

            if not table:
                continue

            rows = table.find_all("tr")[1:]
            for row in rows:
                cols = row.find_all("td")
                if len(cols) < 14:
                    continue

                raw_date = cols[1].text.strip().split()[0]
                try:
                    trade_date = datetime.strptime(raw_date, "%Y-%m-%d")
                except:
                    continue

                ticker = cols[2].text.strip()
                company = cols[3].text.strip()
                insider = cols[5].text.strip()
                title = cols[6].text.strip()
                trade_type = cols[7].text.strip()

                price_text = cols[8].text.strip().replace("$",""
                                        ).replace(",",""
                                        )
                shares_text = cols[9].text.strip().replace(",",""
                                         ).replace("+",""
                                         ).replace("-",""
                                         )
                owned_text  = cols[10].text.strip().replace(",",""
                                         ).replace("+",""
                                         ).replace("-",""
                                         )
                value_text  = cols[12].text.strip().replace("$",""
                                         ).replace(",",""
                                         ).replace("+",""
                                         ).replace("-",""
                                         )

                try:
                    price  = float(price_text)
                    shares = int(shares_text)
                    owned  = int(owned_text)
                    value  = float(value_text)
                except:
                    continue

                all_data.append({
                    "Trade Date":  trade_date,
                    "Ticker":      ticker,
                    "Company":     company,
                    "Insider Name":insider,
                    "Title":       title,
                    "Trade Type":  trade_type,
                    "Price":       price,
                    "Shares":      shares,
                    "Owned":       owned,
                    "Value":       value
                })
            time.sleep(0.5)
        except:
            continue

    os.makedirs("data", exist_ok=True)
    pd.DataFrame(all_data).to_csv("data/historical_insider_trades.csv", index=False)
    print(f"Saved {len(all_data)} records to data/historical_insider_trades.csv.")

if __name__ == "__main__":
    scrape_historical_insiders(pages=100)
