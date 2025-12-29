#!/bin/bash

# Kill background processes on exit
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

# Start Backend
echo "Starting Backend..."
uv run uvicorn src.api.server:app --reload --reload-dir src --reload-dir utils --port 8000 &

# Start Frontend
echo "Starting Frontend..."
cd clarity-ui && npm run dev &

# Wait for both
wait
