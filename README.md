# PPFS

Primitive Python File Server (PPFS) is a file storage system built on [MongoDB GridFS](https://www.mongodb.com/docs/manual/core/gridfs/) capabilities.

It is accessible as a web service made using [FastAPI](https://github.com/tiangolo/fastapi).

## Why?
- I needed some API for storing files to access them using a local web application.
- I wanted to learn FastAPI and have some practice with MongoDB.

## How to

### Prerequisites
- Docker
- Docker compose

### Process
1. Clone the repo
2. Copy/Rename `.env.example` to `.env` and modify it to use your own settings
3. Run `docker compose up -d` to run containers in background

In result, you'll get the running API on the default address <http://localhost:8000>

Interactive docs (Swagger UI) will be available at <http://localhost:8000/docs>
