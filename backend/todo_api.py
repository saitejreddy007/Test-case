from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)
CORS(app)

class Todo(db.Model):
    __tablename__ = 'todos'
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

@app.route('/api/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos]), 200

@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    title = data.get('title')
    if not title or not isinstance(title, str) or not (1 <= len(title) <= 200):
        return jsonify({'error': 'title is required, 1-200 chars, reject empty strings'}), 400
    todo = Todo(title=title)
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict()), 201

@app.route('/api/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = db.session.get(Todo, id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    data = request.get_json()
    title = data.get('title')
    completed = data.get('completed')
    if title is not None:
        if not isinstance(title, str) or not (1 <= len(title) <= 200):
            return jsonify({'error': 'title is required, 1-200 chars, reject empty strings'}), 400
        todo.title = title
    if completed is not None:
        todo.completed = completed
    db.session.commit()
    return jsonify(todo.to_dict()), 200

@app.route('/api/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = db.session.get(Todo, id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted'}), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)