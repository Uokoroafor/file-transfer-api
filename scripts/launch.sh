#!/bin/bash

# This is a script that launches the app on a preconfigured port
echo "Launching app via launch.sh..."

# The default port to run the app on is 8000
PORT=${1:-8000}

# State what port the app is being launched from
echo "Launching app on port $PORT..."

# Run the app via uvicorn on the specified port
poetry run uvicorn file_transfer_api.src.api.api:app --reload --port $PORT &

# Exit with the exit code of the uvicorn command
trap "echo -e '\n App has been terminated...'; exit 0" SIGINT SIGTERM

# Wait for the uvicorn command to finish
wait $!

# Exit with the exit code of the uvicorn command
exit $?