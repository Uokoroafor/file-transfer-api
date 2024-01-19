# File-Transfer-API
This is a file transfer API that allows you to upload and download files from a server.

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

## Usage

### Setting up the Environment

Before running the application, you need to set the environment variables. These are the variables that need to be set:
- **UPLOAD_DIRECTORY**: This is the directory where files will be uploaded to.
- **DOWNLOAD_DIRECTORY**: This is the directory where files will be downloaded to.
- **FILE_STORAGE_TYPE** : This is the type of storage to use. It can be either `local` or `aws`.
- **LOCAL_DATABASE_URL**: This is the url of the local database. It is only required if the `FILE_STORAGE_TYPE` is set to `local`.
- **LOCAL_DATABASE_TABLE_NAME**: This is the name of the table in the local database. It is only required if the `FILE_STORAGE_TYPE` is set to `local`.
- **DATABASE_LOCATION**: This is the location of the database. It is only required if the `FILE_STORAGE_TYPE` is set to `aws`.

You can also update the information by updating the .env.example file and renaming it to .env

### Creating the Database and Table

The database and table can either be created locally or on AWS. If you are using a local database and wish to create the database and table in postgres, you can run the following command:
```
bash scripts/setup_local_database.sh
```
#### TBD: Add instructions for creating the database and table on AWS

[//]: # (If you are using AWS, you can create the database and table by running the following command:)

[//]: # (```)

[//]: # (```)
Note that the database url and table name must be set in the environment variables (see [Setting up the Environment](#setting-up-the-environment)).

### Running the Application
The application can be launched by running the below bash script:
```
bash scripts/launch.sh
```
This will typically launch the application on port 8000. You can then access the application on http://localhost:8000 (or the link provided in the terminal).

The main API actions are:
1. **Upload a file**: This can be done by sending a POST request to the `/upload` endpoint. The request should contain the file to be uploaded in the `file` field. The response will contain the file id of the uploaded file.
2. **Download a file**: This can be done by sending a GET request to the `/download` endpoint. The request should contain the id of the file to be downloaded in the `file_id` field. The response will contain the file to be downloaded.
3. **Delete a file**: This can be done by sending a DELETE request to the `/delete` endpoint. The request should contain the id of the file to be deleted in the `file_id` field. The response will contain a message indicating whether the file was successfully deleted or not.
4. **Rename a file**: This can be done by sending a PUT request to the `/rename` endpoint. The request should contain the id of the file to be renamed in the `file_id` field and the new name of the file in the `new_name` field. The response will contain a message indicating whether the file was successfully renamed or not.
5. **Replace a file**: This can be done by sending a PUT request to the `/replace` endpoint. The request should contain the id of the file to be replaced in the `file_id` field and the new file to replace the old file in the `file` field. The response will contain a message indicating whether the file was successfully replaced or not.

There are also other endpoints that can be used to get information about the files. These can be viewed via the `/docs` endpoint in the browser (via Swagger UI).

To help access the API, a client has been created. The client is located in the `client` folder. This contains helper functions to aid a python client in accessing the API. Use of the client is demonstrated in the `example_usage.py` file.

## Testing
The application can be tested by running the below bash script:
```commandline
bash scripts/run_tests.sh
```
The tests are all location in the `tests` folder within the `app` folder. The tests are written using pytest and can also be run directly using the pytest command in the terminal:
```commandline
pytest
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Author
Ugo Okoroafor - [Uokoroafor](https://github.com/Uokoroafor)

## Built With
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pytest](https://docs.pytest.org/en/stable/)
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Psycopg2](https://www.psycopg.org/docs/)

## Acknowledgements
I would like to thank the great [Sacha Hu](https://github.com/sachahu1) for his tips, time and patience in helping me with this project.
