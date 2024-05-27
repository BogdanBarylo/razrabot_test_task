install:
	poetry install

dev:
	poetry run flask --app razrabot_todo_list:app run