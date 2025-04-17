# Определяем директорию, в которой находится этот скрипт
$DOCERFILE_DIR = (Resolve-Path "$PSScriptRoot\..").Path

# Останавливаем и удаляем контейнер, если он существует
echo "--- Stopped container..."
docker stop um
echo "--- Removed container..."
docker rm um

# Создаем докер образ
echo " --- docker build -t u_manager $DOCERFILE_DIR"
docker build -t u_manager $PSScriptRoot\..

# Запускаем контейнер
echo " --- docker run -d -p 82:8000 --name um u_manager"
docker run -d -p 82:8000 --name um u_manager
