from flask import Flask, render_template, request, redirect, url_for, jsonify
import yfinance as yf

app = Flask(__name__)

# Store stocks that the user has added
user_stocks = {}  
searchable_stocks = []  # Stores tickers of added stocks for search suggestions

# Function to fetch stock data from Yahoo Finance
def get_stock_data(ticker):
    try:
        ticker = ticker.upper()
        stock = yf.Ticker(ticker)

        # Ensure that data is retrieved
        data = stock.info
        if not data or data is None or "regularMarketPrice" not in data:
            return {"error": f"Ticker '{ticker}' not found or data unavailable."}

        return {
            "ticker": ticker,
            "name": data.get("longName", ticker),  # Default to ticker if name is missing
            "price": data.get("regularMarketPrice", 0),
            "market_cap": data.get("marketCap", "N/A"),
            "sector": data.get("sector", "Unknown"),
            "image_url": f"https://logo.clearbit.com/{ticker.lower()}.com",
            "description": data.get("longBusinessSummary", "No description available."),
            "rating": "Hold",  # Default rating
            "shares": 0,       # Default shares
        }
    except Exception as e:
        return {"error": f"Error retrieving stock data: {str(e)}"}



# Home Page - Displays User Stocks
@app.route('/')
def home():
    total_value = sum(stock["shares"] * stock["price"] for stock in user_stocks.values())
    return render_template('home.html', user_stocks=user_stocks, total_value=total_value, searchable_stocks=searchable_stocks)

# Search Stocks - Dynamically Fetches Stocks from Yahoo Finance
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip().upper()
    if not query:
        return redirect(url_for('home'))

    stock_data = get_stock_data(query)
    if "error" in stock_data:
        return render_template('search_results.html', query=query, results=[], error=stock_data["error"])
    
    return render_template('search_results.html', query=query, results=[stock_data], count=1)

# View a Stock (For Stocks Already Added by User)
@app.route('/view/<ticker>')
def view_stock(ticker):
    stock = user_stocks.get(ticker.upper())
    if not stock:
        return "Stock not found", 404
    return render_template('view_stock.html', stock=stock)

# Add Stock Page
@app.route('/add', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        ticker = request.form.get("ticker").upper()
        shares = int(request.form.get("shares", 0))

        if ticker in user_stocks:
            return jsonify({"error": "Stock already added to home screen."}), 400

        stock_data = get_stock_data(ticker)
        if "error" in stock_data:
            return jsonify({"error": stock_data["error"]}), 400

        stock_data["shares"] = shares
        user_stocks[ticker] = stock_data
        searchable_stocks.append(ticker)  # Add to search suggestions

        return redirect(url_for('home'))

    return render_template('add_stock.html')

# Delete Stock from Home Screen
@app.route('/delete_stock/<ticker>', methods=['POST'])
def delete_stock(ticker):
    ticker = ticker.upper()
    if ticker in user_stocks:
        del user_stocks[ticker]
        searchable_stocks.remove(ticker)  # Remove from search suggestions
        return jsonify({"message": "Stock removed from home screen."}), 200
    return jsonify({"error": "Stock not found."}), 404

# Fetch Searchable Stocks for Autocomplete
@app.route('/searchable_stocks', methods=['GET'])
def get_searchable_stocks():
    return jsonify(searchable_stocks)

@app.route('/fetch_stock/<ticker>', methods=['GET'])
def fetch_stock(ticker):
    ticker = ticker.upper()
    stock_data = get_stock_data(ticker)

    if "error" in stock_data:
        return jsonify({"error": stock_data["error"]}), 400  # Return clear error message

    return jsonify(stock_data)

if __name__ == '__main__':
    app.run(debug=True)
