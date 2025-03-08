from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
import os

app = Flask(__name__)

# Set your Polygon.io API key (Replace with your new one)
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY", "8k2Yd07IqDprBnrMMmG5opfVqeMMrA2y")  # Load from environment variable

# In-memory storage for user-added stocks
user_stocks = {}
searchable_stocks = []  # Stores tickers added by users

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY", "8k2Yd07IqDprBnrMMmG5opfVqeMMrA2y")

def get_stock_data(ticker):
    try:
        ticker = ticker.upper()

        # ✅ Fetch company details
        details_url = f"https://api.polygon.io/v3/reference/tickers/{ticker}?apiKey={POLYGON_API_KEY}"
        details_response = requests.get(details_url)
        details_data = details_response.json()

        if "results" not in details_data:
            return {"error": f"Ticker '{ticker}' not found or data unavailable."}

        stock_info = details_data["results"]

        # ✅ Fetch latest stock price and fundamentals
        price_url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?adjusted=true&apiKey={POLYGON_API_KEY}"
        price_response = requests.get(price_url)
        price_data = price_response.json()

        price = price_data["results"][0]["c"] if "results" in price_data and price_data["results"] else 0

        # ✅ Fetch additional fundamentals
        fundamentals_url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/2023-01-01/2024-01-01?adjusted=true&sort=desc&apiKey={POLYGON_API_KEY}"
        fundamentals_response = requests.get(fundamentals_url)
        fundamentals_data = fundamentals_response.json()

        # ✅ Extract fundamental data
        week_high = fundamentals_data["results"][0]["h"] if "results" in fundamentals_data and fundamentals_data["results"] else "N/A"
        week_low = fundamentals_data["results"][0]["l"] if "results" in fundamentals_data and fundamentals_data["results"] else "N/A"

        # ✅ Fetch financials (P/E Ratio, EPS, Dividend Yield)
        financials_url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/year/2023-01-01/2024-01-01?adjusted=true&sort=desc&apiKey={POLYGON_API_KEY}"
        financials_response = requests.get(financials_url)
        financials_data = financials_response.json()

        pe_ratio = financials_data["results"][0].get("pe_ratio", "N/A") if "results" in financials_data and financials_data["results"] else "N/A"
        eps = financials_data["results"][0].get("eps", "N/A") if "results" in financials_data and financials_data["results"] else "N/A"
        dividend_yield = financials_data["results"][0].get("dividend_yield", "N/A") if "results" in financials_data and financials_data["results"] else "N/A"

        return {
            "ticker": stock_info["ticker"],
            "name": stock_info.get("name", ticker),
            "price": price,
            "market_cap": stock_info.get("market_cap", "N/A"),
            "sector": stock_info.get("sector", "Unknown"),
            "image_url": stock_info.get("branding", {}).get("logo_url", f"https://logo.clearbit.com/{ticker.lower()}.com"),
            "description": stock_info.get("description", "No description available."),
            "headquarters": stock_info.get("hq_address", "Unknown"),
            "ceo": stock_info.get("executives", [{}])[0].get("name", "Unknown"),
            "pe_ratio": pe_ratio,
            "eps": eps,
            "dividend_yield": dividend_yield,
            "week_high": week_high,
            "week_low": week_low,
            "rating": "Hold",
            "shares": 0
        }
    except Exception as e:
        return {"error": f"Error retrieving stock data: {str(e)}"}



# Home Page - Displays User Stocks
@app.route('/')
def home():
    total_value = sum(stock["shares"] * stock["price"] for stock in user_stocks.values())
    return render_template('home.html', user_stocks=user_stocks, total_value=total_value, searchable_stocks=searchable_stocks)

# Search Stocks - Dynamically Fetches Stocks from Polygon.io
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip().upper()
    if not query:
        return redirect(url_for('home'))

    stock_data = get_stock_data(query)
    if "error" in stock_data:
        return render_template('search_results.html', query=query, results=[], error=stock_data["error"])
    
    return render_template('search_results.html', query=query, results=[stock_data], count=1)

@app.route('/add', methods=['GET', 'POST'])
def add_stock():
    error_message = None  # ✅ Store error message

    if request.method == 'POST':
        ticker = request.form.get("ticker", "").upper()
        shares = request.form.get("shares", "")

        if not ticker:
            error_message = "Ticker cannot be empty."
        elif not shares.isdigit() or int(shares) < 0:
            error_message = "Shares must be a positive number."
        else:
            stock_data = get_stock_data(ticker)

            if "error" in stock_data:  # ✅ Fix: Correctly check for invalid tickers
                error_message = stock_data["error"]
            elif ticker in user_stocks:
                error_message = "Stock already added to home screen."
            else:
                stock_data["shares"] = int(shares)
                user_stocks[ticker] = stock_data
                searchable_stocks.append(ticker)
                return redirect(url_for('home'))

    return render_template('add_stock.html', error_message=error_message)



# Delete Stock from Home Screen
@app.route('/delete_stock/<ticker>', methods=['POST'])
def delete_stock(ticker):
    ticker = ticker.upper()
    
    if ticker in user_stocks:
        del user_stocks[ticker]
        if ticker in searchable_stocks:
            searchable_stocks.remove(ticker)
        return jsonify({"message": f"Stock {ticker} removed successfully."}), 200
    
    return jsonify({"error": "Stock not found."}), 404



# Fetch Searchable Stocks for Autocomplete
@app.route('/searchable_stocks', methods=['GET'])
def get_searchable_stocks():
    return jsonify(searchable_stocks)

@app.route('/view/<ticker>')
def view_stock(ticker):
    ticker = ticker.upper()
    stock = user_stocks.get(ticker)

    if not stock:
        stock = get_stock_data(ticker)  # Fetch if not in user list
        if "error" in stock:
            return render_template('view_stock.html', error=stock["error"])  # Show error if stock not found

    return render_template('view_stock.html', stock=stock)


@app.route('/edit/<ticker>', methods=['GET', 'POST'])
def edit_stock(ticker):
    ticker = ticker.upper()
    
    if ticker not in user_stocks:
        return "Stock not found", 404

    if request.method == 'POST':
        new_shares = int(request.form.get("shares", user_stocks[ticker]["shares"]))
        new_rating = request.form.get("rating", user_stocks[ticker]["rating"])

        if new_shares < 0:
            return "Shares cannot be negative", 400

        user_stocks[ticker]["shares"] = new_shares
        user_stocks[ticker]["rating"] = new_rating

        return redirect(url_for('view_stock', ticker=ticker))

    return render_template('edit_stock.html', stock=user_stocks[ticker])


@app.route('/update_stock/<ticker>', methods=['POST'])
def update_stock(ticker):
    ticker = ticker.upper()

    if ticker not in user_stocks:
        return jsonify({"error": f"Stock {ticker} not found."}), 404

    try:
        new_shares = request.form.get("shares")
        new_rating = request.form.get("rating")

        if new_shares is None or new_rating is None:
            return jsonify({"error": "Invalid request parameters."}), 400

        new_shares = int(new_shares)

        if new_shares < 0:
            return jsonify({"error": "Shares cannot be negative."}), 400

        # ✅ Update stock data
        user_stocks[ticker]["shares"] = new_shares
        user_stocks[ticker]["rating"] = new_rating

        return jsonify({
            "ticker": ticker,
            "shares": new_shares,
            "rating": new_rating,
            "message": f"Updated {ticker}: {new_shares} shares, Rating: {new_rating}"
        }), 200
    except ValueError:
        return jsonify({"error": "Shares must be a valid number."}), 400






if __name__ == '__main__':
    app.run(debug=True)
