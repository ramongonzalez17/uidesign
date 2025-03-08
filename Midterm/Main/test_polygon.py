import requests
import os

# Set your Polygon API key here
POLYGON_API_KEY = "8k2Yd07IqDprBnrMMmG5opfVqeMMrA2y"  # Replace with your real key

def get_stock_data(ticker):
    """Fetch stock data from Polygon.io API."""
    try:
        ticker = ticker.upper()

        # ✅ Fetch company details
        details_url = f"https://api.polygon.io/v3/reference/tickers/{ticker}?apiKey={POLYGON_API_KEY}"
        details_response = requests.get(details_url)
        details_data = details_response.json()

        if "results" not in details_data or not details_data["results"]:
            return {"error": f"Ticker '{ticker}' not found or does not exist."}

        stock_info = details_data["results"]

        # ✅ Fetch latest stock price
        price_url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?adjusted=true&apiKey={POLYGON_API_KEY}"
        price_response = requests.get(price_url)
        price_data = price_response.json()
        price = price_data["results"][0]["c"] if "results" in price_data and price_data["results"] else None

        # ✅ Fetch fundamentals (52-week high, low, etc.)
        fundamentals_url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/2023-01-01/2024-01-01?adjusted=true&sort=desc&apiKey={POLYGON_API_KEY}"
        fundamentals_response = requests.get(fundamentals_url)
        fundamentals_data = fundamentals_response.json()

        week_high = fundamentals_data["results"][0]["h"] if "results" in fundamentals_data and fundamentals_data["results"] else "N/A"
        week_low = fundamentals_data["results"][0]["l"] if "results" in fundamentals_data and fundamentals_data["results"] else "N/A"

        return {
            "ticker": stock_info["ticker"],
            "name": stock_info.get("name", ticker),
            "price": price,
            "market_cap": format_market_cap(stock_info.get("market_cap", "N/A")),
            "sector": stock_info.get("sector", "Unknown"),
            "image_url": stock_info.get("branding", {}).get("logo_url", f"https://logo.clearbit.com/{ticker.lower()}.com"),
            "description": stock_info.get("description", "No description available."),
            "headquarters": stock_info.get("hq_address", "Unknown"),
            "ceo": stock_info.get("executives", [{}])[0].get("name", "Unknown"),
            "pe_ratio": "N/A",
            "eps": "N/A",
            "dividend_yield": "N/A",
            "week_high": week_high,
            "week_low": week_low,
        }
    except Exception as e:
        return {"error": f"Error retrieving stock data: {str(e)}"}

def format_market_cap(market_cap):
    """Convert market cap to a readable format (e.g., 3.1T for Trillion)."""
    try:
        market_cap = float(market_cap)
        if market_cap >= 1_000_000_000_000:
            return f"{market_cap / 1_000_000_000_000:.1f}T"
        elif market_cap >= 1_000_000_000:
            return f"{market_cap / 1_000_000_000:.1f}B"
        elif market_cap >= 1_000_000:
            return f"{market_cap / 1_000_000:.1f}M"
        return f"{market_cap:.0f}"
    except:
        return "N/A"

# ✅ Run test
if __name__ == "__main__":
    test_tickers = ["AAPL", "NVDA", "TSLA", "RDDT", "INVALIDTICKER"]
    for ticker in test_tickers:
        print(f"\n🔹 **Testing {ticker}**")
        stock_data = get_stock_data(ticker)
        print(stock_data)
