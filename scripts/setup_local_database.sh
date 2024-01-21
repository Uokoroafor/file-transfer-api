#!/bin/bash
# This is a script that sets up the local database by running the setup_local_database.py script in the app directory

# Run the setup_local_database.py script
python database_manager/utils/setup_local_db.py

# Exit with the exit code of the setup_local_database.py script
exit $?