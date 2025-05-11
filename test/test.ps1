# Определяем директорию, в которой находится этот скрипт
$DOCERFILE_DIR = (Resolve-Path "$PSScriptRoot\..").Path

# Останавливаем и удаляем контейнер, если он существует
echo "--- Stopped container..."
docker stop aac
echo "--- Removed container..."
docker rm aac

# Создаем докер образ
echo " --- docker build -t ad_api $DOCERFILE_DIR"
docker build -t ad_api $PSScriptRoot\..

# Запускаем контейнер
echo " --- docker run -d -p 82:8000 --name aac ad_api"
docker run -d -p 82:8000 --name aac ad_api
