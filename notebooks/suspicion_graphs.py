# notebooks/suspicion_graphs.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_top_suspicious(csv_file):
    df = pd.read_csv(csv_file)

    # Pick top 10 suspicious trades
    top_trades = df.head(10)

    plt.figure(figsize=(12,6))
    sns.barplot(
        x="Ticker",
        y="Suspicion Score",
        hue="Insider Name",
        data=top_trades,
        dodge=False
    )

    plt.title("Top 10 Suspicious Insider Trades")
    plt.xlabel("Ticker")
    plt.ylabel("Suspicion Score")
    plt.xticks(rotation=45)
    plt.legend(title="Insider")
    plt.tight_layout()

    # Create a 'plots/' folder if not exists
    if not os.path.exists('plots'):
        os.makedirs('plots')

    plt.savefig('plots/top_suspicious_trades.png')
    plt.show()

if __name__ == "__main__":
    plot_top_suspicious("data/suspicious_insider_trades.csv")
