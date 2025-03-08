import yfinance as yf

# List of tickers to test
test_tickers = ["NVDA", "AAPL", "TSLA", "INVALIDTICKER"]

# Function to fetch stock data from yfinance
def test_yfinance(tickers):
    results = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            data = stock.info

            # Check if valid stock data exists
            if not data or "regularMarketPrice" not in data or data["regularMarketPrice"] is None:
                results[ticker] = {"error": f"Ticker '{ticker}' not found or data unavailable."}
                continue

            results[ticker] = {
                "ticker": ticker,
                "name": data.get("longName", ticker),
                "price": data.get("regularMarketPrice", 0),
                "market_cap": data.get("marketCap", "N/A"),
                "sector": data.get("sector", "Unknown"),
                "image_url": f"https://logo.clearbit.com/{ticker.lower()}.com",
                "description": data.get("longBusinessSummary", "No description available."),
            }
        except Exception as e:
            results[ticker] = {"error": f"Error retrieving stock data: {str(e)}"}

    return results

# Run the test
test_results = test_yfinance(test_tickers)

# Print the results
for ticker, result in test_results.items():
    print(f"\n{ticker}:")
    print(result)
