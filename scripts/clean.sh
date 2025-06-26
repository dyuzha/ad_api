#!/bin/bash

# Удаляем только контейнер (без удаления образа)
docker rm -f aac 2>/dev/null
echo "Контейнер aac удалён"
