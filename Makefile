install:
	poetry install

build:
	./build.sh

dev:
	poetry run flask --app razrabot_todo_list:app run

lint:
	poetry run flake8 razrabot_todo_list