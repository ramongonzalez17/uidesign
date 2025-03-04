# server.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

app = Flask(__name__)

# Tech stock dataset
stocks = [
    {"id": 1, "ticker": "AAPL", "name": "Apple Inc.", "price": 182.50, "market_cap": "2.8T", "sector": "Technology",
     "dividend_yield": 0.60, "pe_ratio": 28.5, "eps": 6.02, "week_high": 198.23, "week_low": 140.20, 
     "headquarters": "Cupertino, CA", "image_url": "https://logo.clearbit.com/apple.com"},
    
    {"id": 2, "ticker": "MSFT", "name": "Microsoft Corporation", "price": 405.20, "market_cap": "3.0T", "sector": "Technology",
     "dividend_yield": 0.80, "pe_ratio": 35.2, "eps": 10.75, "week_high": 420.30, "week_low": 290.10, 
     "headquarters": "Redmond, WA", "image_url": "https://logo.clearbit.com/microsoft.com"},
    
    {"id": 3, "ticker": "NVDA", "name": "NVIDIA Corporation", "price": 775.30, "market_cap": "1.9T", "sector": "Semiconductors",
     "dividend_yield": 0.05, "pe_ratio": 100.3, "eps": 7.95, "week_high": 800.10, "week_low": 230.50, 
     "headquarters": "Santa Clara, CA", "image_url": "https://logo.clearbit.com/nvidia.com"},
    
    {"id": 4, "ticker": "JPM", "name": "JPMorgan Chase & Co.", "price": 185.20, "market_cap": "550B", "sector": "Finance",
     "dividend_yield": 2.80, "pe_ratio": 12.5, "eps": 15.02, "week_high": 200.10, "week_low": 125.80, 
     "headquarters": "New York, NY", "image_url": "https://logo.clearbit.com/jpmorganchase.com"},
    
    {"id": 5, "ticker": "JNJ", "name": "Johnson & Johnson", "price": 156.70, "market_cap": "420B", "sector": "Healthcare",
     "dividend_yield": 2.60, "pe_ratio": 21.4, "eps": 8.60, "week_high": 180.40, "week_low": 145.60, 
     "headquarters": "New Brunswick, NJ", "image_url": "https://logo.clearbit.com/jnj.com"},
    
    {"id": 6, "ticker": "XOM", "name": "Exxon Mobil Corporation", "price": 110.80, "market_cap": "450B", "sector": "Energy",
     "dividend_yield": 3.40, "pe_ratio": 9.8, "eps": 11.23, "week_high": 120.80, "week_low": 85.40, 
     "headquarters": "Irving, TX", "image_url": "https://logo.clearbit.com/exxonmobil.com"},
    
    {"id": 7, "ticker": "KO", "name": "Coca-Cola Co.", "price": 61.20, "market_cap": "260B", "sector": "Consumer Goods",
     "dividend_yield": 3.00, "pe_ratio": 26.2, "eps": 2.35, "week_high": 65.00, "week_low": 53.40, 
     "headquarters": "Atlanta, GA", "image_url": "https://logo.clearbit.com/coca-colacompany.com"},
    
    {"id": 8, "ticker": "WMT", "name": "Walmart Inc.", "price": 155.30, "market_cap": "430B", "sector": "Retail",
     "dividend_yield": 1.50, "pe_ratio": 24.1, "eps": 6.50, "week_high": 165.50, "week_low": 130.20, 
     "headquarters": "Bentonville, AR", "image_url": "https://logo.clearbit.com/walmart.com"},
    
    {"id": 9, "ticker": "TSLA", "name": "Tesla Inc.", "price": 190.00, "market_cap": "600B", "sector": "Automotive",
     "dividend_yield": 0.00, "pe_ratio": 50.3, "eps": 4.25, "week_high": 280.50, "week_low": 160.10, 
     "headquarters": "Austin, TX", "image_url": "https://logo.clearbit.com/tesla.com"},
    
    {"id": 10, "ticker": "DIS", "name": "Walt Disney Company", "price": 108.90, "market_cap": "200B", "sector": "Entertainment",
     "dividend_yield": 1.00, "pe_ratio": 18.6, "eps": 6.40, "week_high": 125.80, "week_low": 90.50, 
     "headquarters": "Burbank, CA", "image_url": "https://logo.clearbit.com/disney.com"},
]




@app.route('/')
def home():
    return render_template('home.html', stocks=stocks)  # Pass full dataset; JS handles sorting

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip().upper()
    if not query:
        return redirect(url_for('home'))

    results = [stock for stock in stocks if query in stock["ticker"] or query in stock["name"].upper()]
    return render_template('search_results.html', query=query, results=results)

@app.route('/view/<int:stock_id>')
def view_stock(stock_id):
    stock = next((s for s in stocks if s["id"] == stock_id), None)
    if not stock:
        return "Stock not found", 404
    return render_template('view_stock.html', stock=stock)

if __name__ == '__main__':
    app.run(debug=True)
