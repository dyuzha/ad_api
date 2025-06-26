#!/bin/bash

# Удаляем контейнер
docker rm -f aac 2>/dev/null

# Удаляем образ
docker rmi ad_api 2>/dev/null

echo "Полная очистка завершена"

