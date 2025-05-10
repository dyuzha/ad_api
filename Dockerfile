# start from base
FROM python:3.9-slim

LABEL maintainer="Dyuzhev Matvey"

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

# start app
CMD ["bash", "run.sh"]
