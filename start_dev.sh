#!/bin/bash
echo "Starting LoL Flex Analyst Services..."

# Start Core API in background
echo "Starting Core API..."
export PYTHONPATH=$PYTHONPATH:.
uvicorn backend.core_api.main:app --host 0.0.0.0 --port 8000 > core_api.log 2>&1 &
CORE_PID=$!
echo "Core API PID: $CORE_PID"

# Start Frontend
echo "Starting Frontend..."
cd frontend
npm install > /dev/null 2>&1
npm run dev > ../frontend.log 2>&1 &
FRONT_PID=$!
echo "Frontend PID: $FRONT_PID"
cd ..

echo "Services started. Check logs for details."
echo "Press CTRL+C to stop."

trap "kill $CORE_PID $FRONT_PID; exit" INT
wait
