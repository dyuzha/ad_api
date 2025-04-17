#!/bin/bash

# Определяем директорию, в которой находится этот скрипт
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Останавливаем и удаляем контейнер, если он существует
echo "--- Stopped container..."
docker stop um || true
echo "--- Removed container..."
docker rm um || true

# Создаем докер образ
echo " --- docker build -t u_manager $SCRIPT_DIR/.."
docker build -t u_manager $SCRIPT_DIR/..

# Запускаем контейнер
echo " --- docker run -d -p 82:8000 --name um u_manager"
docker run -d -p 82:8000 --name um u_manager
