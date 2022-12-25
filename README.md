# file-server

Slightly modified version of [ntdesmond/PPFS](https://github.com/ntdesmond/PPFS).

## Differences

- Settings are configured in [ppfs.yaml](./ppfs.yaml)
  - This allows to create a predefined set of users at startup
  - MongoDB credentials still have to be added to the `.env` file, so that Docker Compose finds them
- Files now have `description` field that includes `ru` and `en` descriptions

## How to

### Prerequisites

- Docker
- Docker Compose

### Process

1. Clone the repo
2. Copy/Rename `.env.example` to `.env` and modify MongoDB credentials
3. Modify [ppfs.yaml](./ppfs.yaml) to use your own settings
4. Run `docker compose up -d` to run containers in background

In result, you'll get the running API on the default address <http://localhost:8000>

Interactive docs (Swagger UI) will be available at <http://localhost:8000/docs>
