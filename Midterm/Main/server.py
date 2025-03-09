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

def format_market_cap(market_cap):
    """Formats market cap into trillions (T) or billions (B)."""
    if market_cap >= 1_000_000_000_000:
        return f"{market_cap / 1_000_000_000_000:.2f}T"
    elif market_cap >= 1_000_000_000:
        return f"{market_cap / 1_000_000_000:.2f}B"
    return f"{market_cap:,}"  # Keep original format for smaller values

def get_stock_data(ticker):
    try:
        ticker = ticker.upper()
        details_url = f"https://api.polygon.io/v3/reference/tickers/{ticker}?apiKey={POLYGON_API_KEY}"
        details_response = requests.get(details_url)
        details_data = details_response.json()

        if "results" not in details_data:
            return {"error": f"Ticker '{ticker}' not found or data unavailable."}

        stock_info = details_data["results"]

        price_url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?adjusted=true&apiKey={POLYGON_API_KEY}"
        price_response = requests.get(price_url)
        price_data = price_response.json()
        price = price_data["results"][0]["c"] if "results" in price_data and price_data["results"] else 0

        branding = stock_info.get("branding", {})
        logo_url = branding.get("logo_url", "").strip()
        icon_url = branding.get("icon_url", "").strip()

        if logo_url:
            logo_url = f"{logo_url}?apiKey={POLYGON_API_KEY}"
        if icon_url:
            icon_url = f"{icon_url}?apiKey={POLYGON_API_KEY}"
        image_url = icon_url if icon_url else logo_url
        if not image_url:
            image_url = "https://via.placeholder.com/150"

        address = stock_info.get("address", {})
        city = address.get("city", "Unknown")
        state = address.get("state", "")
        headquarters = f"{city}, {state}" if state else city

        raw_market_cap = stock_info.get("market_cap", 0)
        formatted_market_cap = format_market_cap(raw_market_cap) if raw_market_cap else "N/A"

        return {
            "ticker": stock_info["ticker"],
            "name": stock_info.get("name", ticker),
            "price": price,
            "market_cap": formatted_market_cap,
            "sector": stock_info.get("sic_description", "Unknown"),
            "image_url": image_url,
            "description": stock_info.get("description", "No description available."),
            "headquarters": headquarters,
            "total_employees": stock_info.get("total_employees", "N/A"),
            "homepage_url": stock_info.get("homepage_url", "#"),
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

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip().upper()
    if not query:
        return redirect(url_for('home'))

    search_url = f"https://api.polygon.io/v3/reference/tickers?search={query}&active=true&limit=10&apiKey={POLYGON_API_KEY}"
    response = requests.get(search_url)
    data = response.json()

    if "results" not in data:
        return render_template('search_results.html', query=query, results=[], error="No matching stocks found.")

    results = []
    for stock_info in data["results"]:
        if stock_info.get("type") != "CS":  # ✅ Exclude ETFs
            continue
        
        # ✅ Fetch full stock data to get description, image, and market cap
        stock_details = get_stock_data(stock_info["ticker"])

        results.append({
            "ticker": stock_info["ticker"],
            "name": stock_info.get("name", "Unknown"),
            "market_cap": stock_details["market_cap"],  # ✅ Use formatted market cap
            "image_url": stock_details["image_url"],  # ✅ Ensure proper image
            "description": stock_details["description"],  # ✅ Ensure description is available
            "sector": stock_details["sector"],
        })

    if not results:
        return render_template('search_results.html', query=query, results=[], error="No matching stocks found. Try a different search.")

    return render_template('search_results.html', query=query, results=results, count=len(results))





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
    owned = ticker in user_stocks  # ✅ Check if the stock is owned

    stock = user_stocks.get(ticker, get_stock_data(ticker))

    if "error" in stock:
        return render_template('view_stock.html', error=stock["error"])

    return render_template('view_stock.html', stock=stock, owned=owned)  # ✅ Pass 'owned' flag




@app.route('/edit/<ticker>', methods=['GET', 'POST'])
def edit_stock(ticker):
    ticker = ticker.upper()

    if ticker not in user_stocks:
        return "Stock not found", 404

    if request.method == 'POST':
        new_shares = request.form.get("shares", user_stocks[ticker]["shares"])
        new_rating = request.form.get("rating", user_stocks[ticker]["rating"])
        new_notes = request.form.get("notes", user_stocks[ticker].get("notes", ""))

        # Ensure shares is a valid number
        try:
            new_shares = int(new_shares)
            if new_shares <= 0:
                return "Shares must be greater than zero", 400
        except ValueError:
            return "Shares must be a valid number", 400

        # ✅ Update stock data
        user_stocks[ticker]["shares"] = new_shares
        user_stocks[ticker]["rating"] = new_rating
        user_stocks[ticker]["notes"] = new_notes

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

        if new_shares <= 0:
            return jsonify({"error": "Shares must be greater than zero."}), 400

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
