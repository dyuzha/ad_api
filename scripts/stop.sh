#!/bin/bash

docker stop aac 2>/dev/null && echo "Контейнер остановлен" || \
    echo "Контейнер не найден"
