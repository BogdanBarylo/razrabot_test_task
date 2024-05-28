from flask import Flask, jsonify, request
from razrabot_todo_list.db import (get_tasks, insert_task,
                                   get_task_by_id, update_task_by_id,
                                   del_task)
from marshmallow import ValidationError
from razrabot_todo_list.validator import TaskSchema, TaskUpdateSchema


app = Flask(__name__)


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Ресурс не найден'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Внутренняя ошибка сервера'}), 500


@app.get('/tasks')
def get_all_tasks():
    tasks = get_tasks()
    return jsonify(tasks)


@app.post('/tasks')
def add_task():
    data = request.json
    schema = TaskSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    title = validated_data['title']
    description = validated_data.get('description', '')
    task = insert_task(title, description)
    if task:
        return jsonify(task), 200
    return jsonify({'error': 'Не удалось добавить задачу'}), 400


@app.get('/tasks/<int:id>')
def get_task(id):
    task = get_task_by_id(id)
    if task:
        return jsonify(task), 200
    return jsonify({'error': 'Задача не найдена'}), 404


@app.put('/tasks/<int:id>')
def update_task(id):
    data = request.json
    schema = TaskUpdateSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    title = validated_data.get('title')
    description = validated_data.get('description', '')
    task = update_task_by_id(id, title, description)
    if task:
        return jsonify(task), 200
    return jsonify({'error': 'Не удалось обновить задачу'}), 400


@app.delete('/tasks/<int:id>')
def delete_task(id):
    if del_task(id):
        return 'Задача успешно удалена', 200
    return jsonify({'error': 'Задача не найдена'}), 404
