from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

@app.route('/calculate_discount', methods=['POST'])
def calculate_discount():
    data = request.get_json()
    original_price = data.get('original_price')
    discount_percentage = data.get('discount_percentage')

    if original_price is None or discount_percentage is None:
        return jsonify({'error': 'Invalid input'}), 400

    final_price = original_price - (original_price * (discount_percentage / 100))
    return jsonify({'final_price': final_price})

if __name__ == '__main__':
    app.run(debug=True)