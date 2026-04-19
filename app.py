from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

class Calculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    result = db.Column(db.Float, nullable=False)

    def __init__(self, type, amount, result):
        self.type = type
        self.amount = amount
        self.result = result

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    calc_type = data.get('type')
    amount = data.get('amount')

    if calc_type == 'tax':
        result = amount * 0.2  # 20% tax
    elif calc_type == 'discount':
        result = amount * 0.1  # 10% discount
    else:
        return jsonify({'error': 'Invalid calculation type'}), 400

    calculation = Calculation(calc_type, amount, result)
    db.create_all()
    db.session.add(calculation)
    db.session.commit()

    return jsonify({'result': result}), 200

if __name__ == '__main__':
    app.run(debug=True)