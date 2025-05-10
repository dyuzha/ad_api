#!/bin/bash

# Проверяем существование образа
if ! docker image inspect ad_api >/dev/null 2>&1; then
  echo "Образ 'ad_api' не найден. Сначала выполните ./build.sh"
  exit 1
fi


# Запуск контейнера
docker run -d -p 82:8000 --name aac ad_api
# Для интерактивного режима замените `-d` на `-it`
