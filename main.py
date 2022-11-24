import yfinance as yf
import pandas as pd

# Columns for CSV are ["ACT Symbol", "Company Name"]
csv = pd.read_csv('./inputs/nyse-test.csv')
tickers = ''

# Outputs "AAPL MFST FBCK ETC"
for index, row in csv.iterrows():
    tickers += row["ACT Symbol"] + ' '

# Gets all data from yfinance with specified tickers
all_ticker_data = yf.Tickers(tickers)
print(all_ticker_data)

# print(all_ticker_data.tickers['WWE'].info.get('marketCap'))

# create empty dataframe
df = pd.DataFrame(columns=["Ticker", "Company Name", "Market Cap"])

for index, row in csv.iterrows():
    ticker = row["ACT Symbol"]
    name = row["Company Name"]
    market_cap = all_ticker_data.tickers[ticker].info.get('marketCap')
    print(ticker, name, market_cap)
    new_row = {
        "Ticker": ticker,
        "Company Name": name,
        "Market Cap": market_cap,
    }
    df = pd.concat([df, pd.DataFrame([new_row])])

df.to_csv('nyse_all_new.csv', index=False)

