from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Global variables to store sales data
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

# Routes

@app.route('/')
def welcome():
    """Render the welcome page."""
    return render_template('welcome.html')

@app.route('/infinity')
def log_sales():
    """Render the log sales page with sales and clients data."""
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
    current_id += 1  # Increment the ID for the next sale
    sales.insert(0, new_sale)  # Add new sale at the top

    # Add new client if not already in list
    if new_sale["client"] not in clients:
        clients.append(new_sale["client"])

    return jsonify(sales=sales, clients=clients)

@app.route('/delete_sale', methods=['POST'])
def delete_sale():
    """Delete a sale by ID and return updated sales list."""
    global sales
    json_data = request.get_json()
    sale_id = json_data["id"]

    # Remove sale with the given ID
    sales = [sale for sale in sales if sale["id"] != sale_id]

    return jsonify(sales=sales)

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True, port=5001)
