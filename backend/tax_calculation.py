from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

@app.route('/calculate_tax', methods=['POST'])
def calculate_tax():
    data = request.get_json()
    income = data.get('income')
    tax_rate = data.get('tax_rate', 0.2)  # Default tax rate is 20%
    if income is None:
        return jsonify({'error': 'Income is required'}), 400
    try:
        income = float(income)  # Ensure income is a float
        tax_rate = float(tax_rate)  # Ensure tax_rate is a float
        tax = income * tax_rate
        return jsonify({'tax': tax}), 200
    except (ValueError, TypeError) as e:
        return jsonify({'error': 'Invalid input'}), 400

if __name__ == '__main__':
    app.run(debug=True)