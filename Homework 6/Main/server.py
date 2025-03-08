# RAMON GONZALEZ RG3474
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

app = Flask(__name__)

# Tech stock dataset
stocks = [
    {"id": 1, "ticker": "AAPL", "name": "Apple Inc.", "price": 182.50, "market_cap": "2.8T", "sector": "Technology",
     "dividend_yield": 0.60, "pe_ratio": 28.5, "eps": 6.02, "week_high": 198.23, "week_low": 140.20, 
     "headquarters": "Cupertino, CA", "image_url": "https://logo.clearbit.com/apple.com",
     "description": "Apple Inc. is a global technology company known for its innovative products such as the iPhone, Mac computers, and iPad. Founded in 1976, Apple has revolutionized consumer technology with sleek design and cutting-edge software. The company continues to push boundaries with advancements in artificial intelligence, augmented reality, and chip manufacturing. With a strong ecosystem of services like the App Store and iCloud, Apple maintains its dominance in the tech industry."},

    {"id": 2, "ticker": "MSFT", "name": "Microsoft Corporation", "price": 405.20, "market_cap": "3.0T", "sector": "Technology",
     "dividend_yield": 0.80, "pe_ratio": 35.2, "eps": 10.75, "week_high": 420.30, "week_low": 290.10, 
     "headquarters": "Redmond, WA", "image_url": "https://logo.clearbit.com/microsoft.com",
     "description": "Microsoft Corporation is a leading technology company that develops software, cloud solutions, and hardware products. It is best known for its Windows operating system, Office productivity suite, and Azure cloud services. Microsoft has diversified into gaming with Xbox and has strengthened its AI capabilities through strategic acquisitions. The company continues to be a dominant force in enterprise software and cloud computing."},

    {"id": 3, "ticker": "NVDA", "name": "NVIDIA Corporation", "price": 775.30, "market_cap": "1.9T", "sector": "Semiconductors",
     "dividend_yield": 0.05, "pe_ratio": 100.3, "eps": 7.95, "week_high": 800.10, "week_low": 230.50, 
     "headquarters": "Santa Clara, CA", "image_url": "https://logo.clearbit.com/nvidia.com",
     "description": "NVIDIA Corporation is a global leader in graphics processing units (GPUs) and artificial intelligence computing. Originally focused on gaming, NVIDIA has expanded into data centers, self-driving cars, and AI research. Its GPUs power some of the most advanced AI models and high-performance computing applications. The company continues to innovate, pushing the boundaries of graphics and AI-driven technology."},

    {"id": 4, "ticker": "JPM", "name": "JPMorgan Chase & Co.", "price": 185.20, "market_cap": "550B", "sector": "Finance",
     "dividend_yield": 2.80, "pe_ratio": 12.5, "eps": 15.02, "week_high": 200.10, "week_low": 125.80, 
     "headquarters": "New York, NY", "image_url": "https://logo.clearbit.com/jpmorganchase.com",
     "description": "JPMorgan Chase & Co. is one of the largest financial institutions in the world, providing banking, investment, and wealth management services. It operates in consumer banking, investment banking, and asset management. The bank plays a significant role in global markets and economic stability. With a strong focus on digital banking and fintech innovation, JPMorgan remains a leader in financial services."},

    {"id": 5, "ticker": "JNJ", "name": "Johnson & Johnson", "price": 156.70, "market_cap": "420B", "sector": "Healthcare",
     "dividend_yield": 2.60, "pe_ratio": 21.4, "eps": 8.60, "week_high": 180.40, "week_low": 145.60, 
     "headquarters": "New Brunswick, NJ", "image_url": "https://logo.clearbit.com/jnj.com",
     "description": "Johnson & Johnson is a multinational healthcare company specializing in pharmaceuticals, medical devices, and consumer health products. It is known for producing life-saving medicines and widely used consumer brands like Tylenol and Band-Aid. The company invests heavily in research and development to advance treatments for various diseases. With a commitment to global health, Johnson & Johnson remains a key player in the healthcare industry."},

    {"id": 6, "ticker": "XOM", "name": "Exxon Mobil Corporation", "price": 110.80, "market_cap": "450B", "sector": "Energy",
     "dividend_yield": 3.40, "pe_ratio": 9.8, "eps": 11.23, "week_high": 120.80, "week_low": 85.40, 
     "headquarters": "Irving, TX", "image_url": "https://logo.clearbit.com/exxonmobil.com",
     "description": "Exxon Mobil Corporation is one of the largest publicly traded oil and gas companies in the world. The company focuses on exploration, production, refining, and distribution of petroleum and natural gas. Exxon is investing in carbon capture technology and alternative energy sources as part of its long-term strategy. Despite market fluctuations, it remains a dominant force in the global energy industry."},

    {"id": 7, "ticker": "KO", "name": "Coca-Cola Co.", "price": 61.20, "market_cap": "260B", "sector": "Consumer Goods",
     "dividend_yield": 3.00, "pe_ratio": 26.2, "eps": 2.35, "week_high": 65.00, "week_low": 53.40, 
     "headquarters": "Atlanta, GA", "image_url": "https://logo.clearbit.com/coca-colacompany.com",
     "description": "Coca-Cola Co. is a global leader in the beverage industry, known for its iconic soft drinks and a diverse portfolio of brands. The company has expanded into bottled water, teas, juices, and energy drinks. Coca-Cola maintains a strong global presence through extensive distribution and marketing strategies. Despite changing consumer preferences, it continues to adapt and innovate in the beverage market."},

    {"id": 8, "ticker": "WMT", "name": "Walmart Inc.", "price": 155.30, "market_cap": "430B", "sector": "Retail",
     "dividend_yield": 1.50, "pe_ratio": 24.1, "eps": 6.50, "week_high": 165.50, "week_low": 130.20, 
     "headquarters": "Bentonville, AR", "image_url": "https://logo.clearbit.com/walmart.com",
     "description": "Walmart Inc. is the world’s largest retailer, operating thousands of stores worldwide. It provides a wide range of products at competitive prices, including groceries, electronics, and apparel. Walmart has also expanded its e-commerce presence to compete with online retailers. Through its scale and supply chain efficiency, the company remains a dominant player in the retail sector."},
    {"id": 9, "ticker": "TSLA", "name": "Tesla Inc.", "price": 190.00, "market_cap": "600B", "sector": "Automotive",
     "dividend_yield": 0.00, "pe_ratio": 50.3, "eps": 4.25, "week_high": 280.50, "week_low": 160.10, 
     "headquarters": "Austin, TX", "image_url": "https://logo.clearbit.com/tesla.com",
     "description": "Tesla Inc. is an American electric vehicle (EV) and clean energy company that has revolutionized the auto industry. Founded by Elon Musk and others, Tesla is known for its high-performance electric cars, energy storage solutions, and solar power innovations. The company has disrupted the traditional auto sector with its self-driving technology, Gigafactories, and direct-to-consumer sales model. Tesla continues to expand its product lineup, including the Cybertruck, and is actively developing AI-driven self-driving capabilities."},

    {"id": 10, "ticker": "DIS", "name": "Walt Disney Company", "price": 108.90, "market_cap": "200B", "sector": "Entertainment",
     "dividend_yield": 1.00, "pe_ratio": 18.6, "eps": 6.40, "week_high": 125.80, "week_low": 90.50, 
     "headquarters": "Burbank, CA", "image_url": "https://logo.clearbit.com/disney.com",
     "description": "The Walt Disney Company is a global entertainment conglomerate known for its iconic films, theme parks, and streaming services. Founded in 1923, Disney has built a vast empire, including Pixar, Marvel, Lucasfilm, and 20th Century Studios. The company has successfully expanded into digital streaming with Disney+, competing with industry giants like Netflix. Disney continues to captivate audiences worldwide with its storytelling, theme park experiences, and blockbuster franchises."}
]

@app.route('/')
def home():
    return render_template('home.html', stocks=stocks)  
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
