from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Task

app = Flask(__name__)
CORS(app)  # Permitir solicitudes desde el frontend

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/jbmal/OneDrive/Escritorio/to-do list-backend/backend/instance/task.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Crear la base de datos (si no existe)
with app.app_context():
    db.create_all()

# Endpoint para obtener todas las tareas
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed} for task in tasks])

# Endpoint para crear una nueva tarea
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = Task(title=data['title'], description=data['description'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task created'}), 201

# Endpoint para actualizar el estado de una tarea
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed
    db.session.commit()
    return jsonify({'message': 'Task updated'})

# Endpoint para eliminar una tarea
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'})

if __name__ == '__main__':
    app.run(debug=True)
