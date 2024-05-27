#!/usr/bin/env bash

make install && poetry run python setup_db.py

#sudo service mysql start