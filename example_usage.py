import os
from client.fastapi_client import FastAPIClient


# Only run this file once the server is running (bash scripts/launch.sh)
client = FastAPIClient()

# Create dummy text files
with open("test.txt", "w") as f:
    f.write("This is a test file")
    f.flush()

with open("test2.txt", "w") as f:
    f.write("This is a test file too")
    f.flush()

# Upload the file
response_1 = client.upload_file("test.txt")

# Get JSON response
print(response_1.json())

# Get raw response
print(response_1.content)
response_1 = response_1.json()

# Download the file
response_2 = client.download_file(response_1["file_id"])
print(response_2.json())

# Rename a file
response_3 = client.rename_file(response_1["file_id"], response_1["file_id"][:-1])
print(response_3.json())

# Replace a file
response_4 = client.replace_file(response_1["file_id"][:-1], "test2.txt")
print(response_4.json())

# Delete a file
response_5 = client.delete_file(response_1["file_id"][:-1])
print(response_5.json())

# Delete the test files
os.remove("test.txt")
os.remove("test2.txt")
