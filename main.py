import yfinance as yf
import pandas as pd

# Columns for CSV are ["ACT Symbol", "Company Name"]
csv = pd.read_csv('./inputs/nyse-test.csv')
tickers = ''

# Outputs "AAPL MFST FBCK ETC"
for index, row in csv.iterrows():
    tickers += row["ACT Symbol"] + ' '

# Gets all data from yfinance with specified tickers
all_ticker_data = yf.Tickers(tickers).tickers

# print(all_ticker_data.tickers['WWE'].info.get('marketCap'))

# create empty dataframe
df = pd.DataFrame(columns=["Ticker", "Company Name", "Market Cap", "Website"])

for index, row in csv.iterrows():
    ticker = row["ACT Symbol"]
    name = row["Company Name"]
    yfinance_info = all_ticker_data[ticker].info
    market_cap = yfinance_info.get('marketCap')
    website = yfinance_info.get('website')
    print(ticker, name, market_cap)
    new_row = {
        "Ticker": ticker,
        "Company Name": name,
        "Market Cap": market_cap,
        "Website": website
    }
    df = pd.concat([df, pd.DataFrame([new_row])])

df.to_csv('nyse_all_new.csv', index=False)

