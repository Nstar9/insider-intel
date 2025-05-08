import pandas as pd

def calculate_suspicion_score(csv_file):
    df = pd.read_csv(csv_file)

    if df.empty:
        print("⚠️ Warning: The file is empty! Nothing to score.")
        return

    scores = []

    for idx, row in df.iterrows():
        try:
            shares_traded = int(row['Shares'])
            trade_type = row['Trade Type']
            
            score = shares_traded / 1000  # normalize
            if "Buy" in trade_type:
                score += 20  # Bonus if it's a buy

            scores.append({
                "Ticker": row['Ticker'],
                "Trade Date": row['Trade Date'],
                "Insider Name": row['Insider Name'],
                "Trade Type": trade_type,
                "Shares Traded": shares_traded,
                "Suspicion Score": round(score, 2)
            })

        except Exception as e:
            print(f"Error processing {row}: {e}")
            continue

    scores_df = pd.DataFrame(scores)
    scores_df = scores_df.sort_values(by="Suspicion Score", ascending=False)
    scores_df.to_csv("data/suspicious_trades.csv", index=False)
    print(f"✅ Saved suspicious trades ranked by score.")

if __name__ == "__main__":
    calculate_suspicion_score("data/historical_insider_trades.csv")
