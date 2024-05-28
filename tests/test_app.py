from flask.testing import FlaskClient
import pytest
from razrabot_todo_list import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_add_task(truncate_db, testing_task, client: FlaskClient):
    response = client.post('/tasks', json=testing_task)
    assert response.status_code == 200
    response_data = response.json
    assert 'id' in response_data
    assert response_data['title'] == testing_task['title']
    assert response_data['description'] == testing_task['description']
    assert 'created_at' in response_data
    assert 'updated_at' in response_data


def test_invalid(truncate_db, client: FlaskClient):
    response = client.post('/tasks', json={'description': 'invalid'})
    assert response.status_code == 400
    assert 'Не удалось добавить задачу' in response.json.values()


def test_get_nonexistent_task(truncate_db, client):
    response = client.get('/tasks/100')
    assert response.status_code == 404


def test_get_all_tasks(truncate_db, client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    tasks = response.json
    for task in tasks:
        assert 'id' in task
        assert 'title' in task
        assert 'description' in task
        assert 'created_at' in task
        assert 'updated_at' in task


def test_update_task(truncate_db, testing_task, client):
    create_response = client.post('/tasks', json=testing_task)
    task_id = create_response.json['id']
    update_data = {'title': 'Updated Test Task', 'description': 'This is an updated test task description.'}
    update_response = client.put(f'/tasks/{task_id}', json=update_data)
    assert update_response.status_code == 200
    updated_task = update_response.json
    assert updated_task['id'] == task_id
    assert updated_task['title'] == update_data['title']
    assert updated_task['description'] == update_data['description']
    assert 'created_at' in updated_task
    assert 'updated_at' in updated_task
    get_response = client.get(f'/tasks/{task_id}')
    assert get_response.status_code == 200
    assert get_response.json['title'] == update_data['title']
    assert get_response.json['description'] == update_data['description']


def test_invalid_update_task(truncate_db, testing_task, client):
    create_response = client.post('/tasks', json=testing_task)
    task_id = create_response.json['id']
    update_data = {'title': '', 'description': 'Updated description.'}
    update_response = client.put(f'/tasks/{task_id}', json=update_data)
    assert update_response.status_code == 400
    assert 'Не удалось обновить задачу' in update_response.json.values()
    get_response = client.get(f'/tasks/{task_id}')
    assert get_response.status_code == 200
    assert get_response.json['title'] == testing_task['title']
    assert get_response.json['description'] == testing_task['description']


def test_delete_task(truncate_db, testing_task, client):
    create_response = client.post('/tasks', json=testing_task)
    task_id = create_response.json['id']
    delete_response = client.delete(f'/tasks/{task_id}')
    assert delete_response.status_code == 200
    assert delete_response.json['message'] == 'Запись успешно удалена'
    get_response = client.get(f'/tasks/{task_id}')
    assert get_response.status_code == 404
    assert get_response.json['error'] == 'Задача не найдена'