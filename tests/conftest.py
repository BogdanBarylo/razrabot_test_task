from razrabot_todo_list.db import clear_db, insert_task
from pytest import fixture


@fixture
def truncate_db():
    yield
    clear_db()


@fixture
def testing_task():
    return {
        "title": "Test Task",
        "description": "This is a test task description."}


@fixture
def added_task(testing_task):
    task = insert_task(testing_task["title"], testing_task["description"])
    yield task
    clear_db()
