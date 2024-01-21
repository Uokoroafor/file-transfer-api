#!/bin/bash

# This is a script that launches the app on a preconfigured port

# The default port to run the app on is 8000
PORT=${1:-8000}

# Run the app via uvicorn on the specified port
uvicorn api.api:app --reload --port $PORT