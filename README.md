Intelligent Book Management System (AI + FastAPI + PostgreSQL)

An intelligent, cloud-ready book management system built with:
- **FastAPI (async REST API)**
- **PostgreSQL (async SQLAlchemy)**
- **JWT Authentication (Role-based)**
- **Local Llama3 AI Model Integration (Ollama)**
- **Docker-ready deployment**

Quickstart (Docker)

1. Install Docker & Docker Compose
2. Clone repo and cd into it
3. Ensure Ollama is running on host (see below)
4. Start stack:
   ```
   docker-compose up --build
   ```
5. Open API docs at `http://localhost:8000/docs`

Ollama (local Llama3) example
Install and run Ollama on host machine, then run a Llama3 model:
```
# install ollama per docs, then:
ollama pull llama3
ollama run llama3
```
Ensure `LLAMA_ENDPOINT` in `.env` points to your Ollama HTTP endpoint (host.docker.internal is useful when running app in Docker).

Tests
```
pip install -r requirements.txt
pytest -q
```
