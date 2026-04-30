from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)
CORS(app)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'completed': self.completed,
            'created_at': self.created_at.isoformat()
        }

with app.app_context():
    db.create_all()

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks]), 200

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    if not title or not isinstance(title, str) or not (1 <= len(title) <= 200):
        return jsonify({'error': 'title is required, 1-200 chars, reject empty strings'}), 400
    task = Task(title=title)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@app.route('/api/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = db.session.get(Task, id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    data = request.get_json()
    title = data.get('title')
    completed = data.get('completed')
    if title is not None:
        if not isinstance(title, str) or not (1 <= len(title) <= 200):
            return jsonify({'error': 'title must be 1-200 chars'}), 400
        task.title = title
    if completed is not None:
        task.completed = completed
    db.session.commit()
    return jsonify(task.to_dict()), 200

@app.route('/api/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = db.session.get(Task, id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'}), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True)