FROM python:3.10
WORKDIR /app

COPY ./docker/requirements.txt /tmp
RUN python -m venv .venv && \
    ./.venv/bin/python -m pip install --no-cache-dir --upgrade pip setuptools wheel && \
    ./.venv/bin/python -m pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

RUN groupadd app && useradd app -g app

COPY ./ppfs ./ppfs
COPY ./config ./config

USER app
EXPOSE 8000

ENTRYPOINT ["./.venv/bin/gunicorn", "--config", "./config/gunicorn.conf.py", "ppfs:app"]