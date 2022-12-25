FROM python:3.10 as builder
WORKDIR /app

# Install requirements
COPY ./docker/requirements.txt /tmp
RUN python -m venv .venv && \
    ./.venv/bin/python -m pip install --no-cache-dir --upgrade pip setuptools wheel && \
    ./.venv/bin/python -m pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt


FROM python:3.10-slim as runner
WORKDIR /app

# Create non-privileged user
RUN addgroup app && useradd app -g app

# Copy the venv and the app
COPY --from=builder /app/.venv /app/.venv
COPY ./ppfs ./ppfs
COPY ./config ./config

USER app
EXPOSE 8000

ENTRYPOINT ["./.venv/bin/gunicorn", "--config", "./config/gunicorn.conf.py", "ppfs:app"]