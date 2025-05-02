#!/usr/bin/env bash
set -e  # exit script if any command fails
ollama serve &

echo "Waiting for ollama to start..."
sleep 5

echo "Starting Python app..."
uv run python -m app.main

echo "Python app has exited."