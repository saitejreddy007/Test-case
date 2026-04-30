from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = Task(description=data['description'], created_at=datetime.utcnow())
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'description': 'Task is created and returned with 201 status'}), 201

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)