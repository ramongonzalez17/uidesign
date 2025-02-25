from flask import Flask, render_template, request, jsonify
import os
app = Flask(__name__)

current_id = 4
sales = [
    {"id": 1, "salesperson": "James D. Halpert", "client": "Shake Shack", "reams": 1000},
    {"id": 2, "salesperson": "Stanley Hudson", "client": "Toast", "reams": 4000},
    {"id": 3, "salesperson": "Michael G. Scott", "client": "Computer Science Department", "reams": 10000},
]

clients = [
    "Shake Shack", "Toast", "Computer Science Department", "Teacher's College",
    "Starbucks", "Subsconsious", "Flat Top", "Joe's Coffee",
    "Max Caffe", "Nussbaum & Wu", "Taco Bell"
]

# 

@app.route('/')
def welcome():
    """Render the welcome page."""
    return render_template('welcome.html')

@app.route('/infinity')
def log_sales():
    template_path = os.path.join(app.root_path, "templates", "log_sales.html")
    if not os.path.exists(template_path):
        return "⚠️ ERROR: log_sales.html NOT FOUND!", 500  # Return error if missing
    
    print("✅ log_sales.html is being rendered")
    return render_template('log_sales.html', sales=sales, clients=clients)

# API Routes for sales management

@app.route('/save_sale', methods=['POST'])
def save_sale():
    """Save a new sale and return updated sales and clients lists."""
    global sales, clients, current_id

    json_data = request.get_json()
    new_sale = {
        "id": current_id,
        "salesperson": json_data["salesperson"],
        "client": json_data["client"],
        "reams": json_data["reams"]
    }
    current_id += 1 
    sales.insert(0, new_sale)  

    if new_sale["client"] not in clients:
        clients.append(new_sale["client"])

    return jsonify(sales=sales, clients=clients)

@app.route('/delete_sale', methods=['POST'])
def delete_sale():
    global sales
    json_data = request.get_json()
    sale_id = json_data["id"]

    sales = [sale for sale in sales if sale["id"] != sale_id]

    return jsonify(sales=sales)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
