import os
from file_transfer_api.src.client.client import APIClient

# Initialise the Client
client = APIClient(error_logger_path="logs/errors.log")
# It will create a logger in the specified folders if they do not exist

# Let's create a test file and test the client
with open("test.txt", "wb") as file:
    file.write(b"Hello, World!")

# Upload the file onto the server and update the database
response1 = client.upload_file("test.txt")

# Download the file from the database and return raw bytes
response2 = client.download_file(response1.file_id)

# Change the file name saved in the database
response3 = client.rename_file(response1.file_id, "test2.png")

# Delete the file from the server and the database
response4 = client.delete_file(response1.file_id)

# Delete the test file
os.remove("test.txt")
