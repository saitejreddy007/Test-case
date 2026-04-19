from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

class DiscountCalculator:
    @staticmethod
    def calculate_discount(amount, discount_rate):
        if amount < 0 or discount_rate < 0:
            raise ValueError('Amount and discount rate must be non-negative.')
        discount_amount = amount * (discount_rate / 100)
        return discount_amount

@app.route('/calculate_discount', methods=['POST'])
def calculate_discount():
    data = request.get_json()
    amount = data.get('amount')
    discount_rate = data.get('discount_rate')

    if amount is None or discount_rate is None:
        return jsonify({'error': 'Amount and discount rate are required.'}), 400

    try:
        discount_amount = DiscountCalculator.calculate_discount(amount, discount_rate)
        return jsonify({'discount_amount': discount_amount})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)