#!/bin/sh
ollama serve &
sleep 5  # Wait for Ollama to start
uvicorn main:app --host 0.0.0.0 --port ${EMBEDDER_PORT} &
wait