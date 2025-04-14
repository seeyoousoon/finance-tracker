from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

#Production use a database or Firestore
transactions_list = []

# ---------------------------------------------------
# 1. /save-transaction
# ---------------------------------------------------
@app.route('/save-transaction', methods=['POST'])
def save_transaction():
    data = request.get_json()
    print("Got data in /save-transaction:", data)

    title = data.get("title", "")
    amount = data.get("amount", 0)
    category = data.get("category", "Uncategorized")

    # For simplicity, just append to our in-memory list
    new_tx = {
        "title": title,
        "amount": amount,
        "category": category
    }
    transactions_list.append(new_tx)
    print("Transaction saved:", new_tx)

    # Return success
    return jsonify({"success": True})


# ---------------------------------------------------
# 2. /auto-tag
# ---------------------------------------------------
# This route returns a predicted category for a transaction title.
@app.route('/auto-tag', methods=['POST'])
def auto_tag():
    data = request.get_json()
    print("Received data for /auto-tag:", data)

    # Convert title to lowercase for case-insensitive matching.
    title = data.get("title", "").lower()

    # Set default category.
    category = "Miscellaneous"

    # Check for specific categories in order:
    if "rent" in title:
        category = "Rent"
    elif "clothing" in title:
        category = "Clothing"
    # Check for food-related keywords.
    elif any(kw in title for kw in ["food", "starbucks", "grocery", "restaurant"]):
        category = "Food"
    # Check for utilities using specific keywords.
    elif any(kw in title for kw in ["electricity", "water", "phone"]):
        category = "Utilities"

    print("Returning auto-tag category:", category)
    return jsonify({"category": category})
# ---------------------------------------------------
# 3. /detect-anomaly
# ---------------------------------------------------
@app.route('/detect-anomaly', methods=['POST'])
def detect_anomaly():
    data = request.get_json()
    print("Got data for /detect-anomaly:", data)

    try:
        amount = float(data.get("amount", 0))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid amount provided"}), 400

    # Example logic: mark anything above 500 as anomaly
    anomaly_detected = amount > 500

    print("Anomaly:", anomaly_detected)
    return jsonify({"anomaly": anomaly_detected})


# ---------------------------------------------------
# 4. /smart-budget
# ---------------------------------------------------
@app.route('/smart-budget', methods=['POST'])
def smart_budget():
    data = request.get_json()
    print("Got data for /smart-budget:", data)

    try:
        income = float(data.get("income", 0))
        expenditure = float(data.get("expenditure", 0))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input"}), 400

    # Example logic: recommend saving 20% of income if income > expenditure
    if income <= expenditure:
        suggestion = "Consider reducing expenses or increasing income."
    else:
        saving = income * 0.20
        suggestion = f"We suggest saving about ${saving:.2f}."

    print("Returning smart budget suggestion:", suggestion)
    return jsonify({"suggestion": suggestion})


# ---------------------------------------------------
# 5. /transactions
# ---------------------------------------------------
@app.route('/transactions', methods=['GET'])
def get_transactions():
    # Return the in-memory list of transactions
    print("Returning transactions_list:", transactions_list)
    return jsonify(transactions_list)


# ---------------------------------------------------
# 6. /expense-forecast
# ---------------------------------------------------
@app.route('/expense-forecast', methods=['GET'])
def expense_forecast():
    # Example of dummy forecast data
    # In production, load a model or have advanced logic
    forecast_data = [
        {"date": "2025-05-01", "expense": 900},
        {"date": "2025-06-01", "expense": 1000},
        {"date": "2025-07-01", "expense": 1100},
        {"date": "2025-08-01", "expense": 950},
        {"date": "2025-09-01", "expense": 1200},
    ]
    print("Returning expense forecast data.")
    return jsonify(forecast_data)

# ---------------------------------------------------
# Clears all the transcation
transactions = []

@app.route('/clear-transactions', methods=['DELETE'])
def clear_transactions():
    global transactions
    transactions.clear()
    return jsonify({'status': 'cleared'}), 200

# ---------------------------------------------------
# MAIN
# ---------------------------------------------------
if __name__ == '__main__':
    # Debug mode for local testing
    app.run(debug=True)

