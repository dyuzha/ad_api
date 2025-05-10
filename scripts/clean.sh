#!/bin/bash

# Удаляем контейнер
docker rm aac 2>/dev/null

# Удаляем образ
docker rmi ad_api 2>/dev/null

echo "Очистка завершена"
