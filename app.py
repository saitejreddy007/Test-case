from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

class TaxCalculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    tax_rate = db.Column(db.Float, nullable=False)
    tax_amount = db.Column(db.Float, nullable=False)

    def __init__(self, amount, tax_rate):
        self.amount = amount
        self.tax_rate = tax_rate
        self.tax_amount = self.calculate_tax()

    def calculate_tax(self):
        return self.amount * (self.tax_rate / 100)

@app.route('/calculate_tax', methods=['POST'])
def calculate_tax():
    data = request.get_json()
    amount = data.get('amount')
    tax_rate = data.get('tax_rate')

    if amount is None or tax_rate is None:
        return jsonify({'error': 'Amount and tax rate are required'}), 400

    tax_calculation = TaxCalculation(amount, tax_rate)
    db.session.add(tax_calculation)
    db.session.commit()
    return jsonify({'tax_amount': tax_calculation.tax_amount}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)