# File-Transfer-API
This is a file transfer API that allows one to upload and download files from a server either locally or on AWS. Think of it as a personal mini Dropbox or Google Drive. The API is built using [FastAPI](https://fastapi.tiangolo.com/) and [SQLAlchemy](https://www.sqlalchemy.org/). The API is also tested using [Pytest](https://docs.pytest.org/en/stable/).


## Table of Contents
1. [Installation](#installation)
1. [Usage](#usage)
    1. [Setting up the Environment](#setting-up-the-environment)
    2. [Creating the Database and Table](#creating-the-database-and-table)
    3. [Launching the Application](#launching-the-application)
    4. [Using the Client](#using-the-client)
1. [Testing](#testing)
2. [Contributing](#contributing)
1. [Author](#author)
1. [Built With](#built-with)
1. [Acknowledgements](#acknowledgements)


## Installation
1. Clone the repository
    ```
    git clone https://github.com/Uokoroafor/file-transfer-api
    cd file-transfer-api
    ```
2. Install the dependencies. The project uses [poetry](https://python-poetry.org/) to manage dependencies and as such, dependencies can be installed by running:
    ```
    poetry install
    ```
3. Activate the virtual environment if not already activated. This can be done by running:
    ```
    poetry shell
    ```



## Usage

### Setting up the Environment

Before running the application, you need to set the environment variables. First set whether you want to use local or AWS storage and database. This can be done by setting the values of the variables below:
- **FILE_STORAGE_TYPE** : This is the type of storage to use. It can be either `local` or `aws`.
- **DATABASE_LOCATION**: This is the location of the database. It can be either `local` or `aws`.


The variables below need to be set if you are using local storage and a local database:
- **UPLOAD_DIRECTORY**: This is the directory where files will be uploaded to.
- **DOWNLOAD_DIRECTORY**: This is the directory where files will be downloaded to.
- **LOCAL_DATABASE_URL**: This is the url of the local database. It is only required if the `FILE_STORAGE_TYPE` is set to `local`.

Note that the table name is set to `files` by default. This can be changed by setting the `LOCAL_DATABASE_TABLE_NAME` environment variable.

The variables below need to be set if you are using AWS:
- **TBD: AWS variables**

You can also update the information by updating the .env.example file and renaming it to .env

### Creating the Database and Table

The database and table can either be created locally or on AWS. If you are using a local database and wish to create the database and table in postgres, you can run the following command:
```
poetry run scripts/setup_local_database.sh
```
Note that the database url must be set in the environment variables (see [Setting up the Environment](#setting-up-the-environment)).

#### TBD: Creating the database and table on AWS

[//]: # (If you are using AWS, you can create the database and table by running the following command:)

[//]: # (```)

[//]: # (```)

### Launching the Application
The application can be launched by running the below bash script:
```
poetry run scripts/launch.sh
```
This will launch the application on port 8000. You can then access the application on http://localhost:8000 (or the link provided in the terminal). To launch from a different port, include the port number as an argument to the script (e.g. for port 8080):
``` 
poetry run scripts/launch.sh 8080
```
### API Actions
[//]: # (The main API actions are:)

[//]: # (1. **Upload a file**: This can be done by sending a POST request to the `/upload` endpoint. The request should contain the file to be uploaded in the `file` field. The response will contain the file id of the uploaded file.)

[//]: # (2. **Download a file**: This can be done by sending a GET request to the `/download` endpoint. The request should contain the id of the file to be downloaded in the `file_id` field. The response will contain the file to be downloaded.)

[//]: # (3. **Delete a file**: This can be done by sending a DELETE request to the `/delete` endpoint. The request should contain the id of the file to be deleted in the `file_id` field. The response will contain a message indicating whether the file was successfully deleted or not.)

[//]: # (4. **Rename a file**: This can be done by sending a PUT request to the `/rename` endpoint. The request should contain the id of the file to be renamed in the `file_id` field and the new name of the file in the `new_name` field. The response will contain a message indicating whether the file was successfully renamed or not.)

[//]: # (5. **Replace a file**: This can be done by sending a PUT request to the `/replace` endpoint. The request should contain the id of the file to be replaced in the `file_id` field and the new file to replace the old file in the `file` field. The response will contain a message indicating whether the file was successfully replaced or not.)

FastAPI provides a documentation page (via [Swagger UI](https://swagger.io/tools/swagger-ui/)) that can be used to view the API endpoints. This can be accessed via the `/docs` endpoint in the browser.

## Using the Client
The provided client in the `client` folder simplifies interactions with the API. It offers convenient helper functions for Python clients. See `example_usage.py` for detailed examples. Key functionalities include initializing the client, uploading, downloading, deleting, and renaming files.
1. **Initialising the Client**
   ```python3
   from client.client import APIClient
   
   client = APIClient()  # Defaults to 'http://localhost:8000', override with `APIClient('your_url')`
   ```

2. **Uploading a File**
   ```python3
   file_path = 'test_file.txt'
   
   File_ID_and_Path = client.upload_file(file_path)
   # Response: Dataclass with 'file_id' and 'file_path' attributes
   ```

3. **Downloading a File**
   ```python3
   file_id = 'test_file_id'
   
   raw_response = client.download_file(file_id)
   # Response: Raw server response(bytes), save or process as needed
   ```
4. **Deleting a File**
   ```python3
   file_id = 'test_file_id'
   
   response = client.delete_file(file_id)
   # Response: Success or error message
   ```
5. **Renaming a File**
   ```python3
   file_id = 'test_file_id'
   new_name = 'new_test_file.txt'
   
   response = client.rename_file(file_id, new_name)
   # Response: Success or error message
   ```

### Error Handling
When an error occurs during API interaction, the client returns an ErrorResponse. This response object contains a status code and an error message, providing details about the error.

#### Example Error
For instance, attempting to download a non-existent file results in the following ErrorResponse:

```python3
response = client.download_file('non_existent_file_id')
# Response: ErrorResponse(status_code=404, message=f"No such file or directory at {upload_path}/non_existent_file_id")
```
All errors are logged in the `logs` folder for further analysis.

#### Handling Errors:

[//]: # (- *Check the Status Code*: Use the status_code to identify the type of error &#40;e.g., 404 for not found, 500 for server errors&#41;.)

[//]: # (- *Check the Error Message*: The error message provides additional details about the error. For example, if the error message contains the string 'No such file or directory', then the file does not exist on the server.)

[//]: # (- *Check the Logs*: The logs folder contains a log of all errors that have occurred. This can be used to identify the cause of the error.)

- *Check the Status Code*: Use status_code to identify the error type (404 for not found, 500 for server errors, etc.).
- *Understand the Error Message*: It provides context about the error. E.g., 'No such file or directory' indicates a missing file.
- *Review Error Logs*: Refer to the logs folder for a history of errors, which can help in diagnosing persistent or complex issues.
- *Corrective Actions*: For a 404 error, verify the file ID or check if the file exists. For a 500 error, consider retrying the request or checking that there are no internal permission issues.

By following these steps, users can effectively manage and resolve errors encountered while using the API. Please contact the developer ([me](https://github.com/Uokoroafor)) for further assistance.

## Testing
The tests are all location in the `tests` folder and are written using pytest. They can also be run directly using the pytest command in the terminal:
```commandline
pytest
```

## Contributing
As this project is still in development, it is currently not open to contributions. However, if you have any suggestions or feedback, please feel free to contact me.

## Author
Ugo Okoroafor - [Uokoroafor](https://github.com/Uokoroafor)

## Built With
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

[//]: # (- [Boto3]&#40;https://boto3.amazonaws.com/v1/documentation/api/latest/index.html&#41;)


## Acknowledgements
I would like to thank the great [Sacha Hu](https://github.com/sachahu1) for his tips, time and patience - he was an immense help with this project.
