from flask import Flask, request, jsonify
import database # Reusing our secure database engine
import security # Reusing our encryption engine

app = Flask(__name__)

# Initialize database tables on server startup
database.setup_secure_db()

@app.route('/expense', methods=['POST'])
def add_expense():
    """An endpoint that allows clients to send data over HTTP."""
    data = request.get_json()
    
    # Validation check
    if not data or 'amount' not in data or 'category' not in data:
        return jsonify({"error": "Bad Request. Missing fields."}), 400
        
    try:
        amount = float(data['amount'])
        category = str(data['category'])
        
        # Log it securely using our existing architectural layers
        database.log_secure_expense(amount, category)
        return jsonify({"message": "Transaction encrypted and saved to server cloud!"}), 201
        
    except ValueError:
        return jsonify({"error": "Invalid data format."}), 400

@app.route('/summary', methods=['GET'])
def view_summary():
    """An endpoint that returns the processed financial dashboard data."""
    summary_data = database.get_secure_summary()
    
    # Convert dict items to a serializable list for the network transfer
    report = [{"category": cat, "total": total} for cat, total in summary_data]
    return jsonify(report), 200

if __name__ == '__main__':
    # Run server locally on port 5000
    app.run(port=5000, debug=True)
