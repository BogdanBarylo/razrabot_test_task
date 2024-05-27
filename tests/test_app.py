from flask.testing import FlaskClient
import pytest
import re
from razrabot_todo_list import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client