FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir chromadb[server]

EXPOSE 8000

CMD ["chromadb", "run", "--host", "0.0.0.0", "--port", "8000"]
