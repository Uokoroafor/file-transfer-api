#!/bin/bash
# This is a script that sets up the local database by running the setup_local_database.py script in the app directory

# State that the local database is being set up
echo "Setting up local database..."

# Run the setup_local_database.py script
poetry run python -m file_transfer_api.src.database_manager.utils.setup_local_db

# Capture exit code
EXIT_CODE=$?

# If the exit code is 0, state that the local database has been set up
if [ $EXIT_CODE -eq 0 ]; then
    echo "Local database has been set up!"
else
    echo "Local database setup failed!"
fi

# Exit with the exit code of the setup_local_database.py script
exit $EXIT_CODE