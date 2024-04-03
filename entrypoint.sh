#!/bin/bash

echo "Waiting for MySQL..."
while ! nc -z mysqlDB 3306; do
  sleep 1
done
echo "MySQL started"

alembic upgrade head

python populate_data.py

exec uvicorn app:app --host 0.0.0.0 --port 9000
