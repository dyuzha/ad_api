# start from base
FROM python:3.9-slim

LABEL maintainer="Dyuzhev Matvey"

WORKDIR /app

COPY app/ .

RUN pip install --no-cache-dir -r requirements.txt

# start app
CMD ["bash", "run.sh"]
