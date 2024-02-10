# File-Transfer-API
This is a three-part project that seeks to build out a file management system (akin to Dropbox or Google Drive) that will eventually be hosted on AWS.

The three parts are:
1. **File-Transfer-API**: This is the backend API that allows one to upload and download files from a server either locally or on AWS. The API is built using [FastAPI](https://fastapi.tiangolo.com/) and [SQLAlchemy](https://www.sqlalchemy.org/). The API is also tested using [Pytest](https://docs.pytest.org/en/stable/).
2. **Cloudformation_Architecture**: This is the AWS infrastructure that will be used to host the API. It is built using [AWS Cloudformation](https://aws.amazon.com/cloudformation/).
3. **Frontend**: This is the frontend that will be used to interact with the API. It is built using [React](https://reactjs.org/).

## Project Roadmap
Note that while the below roadmap is listed in phases,there is a lot of overlap and development will be done in parallel.

**Phase 1**: Build the File-Transfer-API and test it locally.
   - [x] Build the API
   - [x] Test the API locally
   - [x] Write tests for the API
   - [x] Document the API
   - [ ] Ongoing enhancements to the API

**Phase 2**: Build the Cloudformation_Architecture and test it on AWS.
   - [ ] Build the AWS infrastructure in Cloudformation
   - [ ] Expand the API to work with AWS
   - [ ] Test the infrastructure on AWS
   - [ ] Document the infrastructure
   - [ ] Dockerize the API

**Phase 3**: Build the Frontend and test it locally.
   - [ ] Build the frontend
   - [ ] Test the frontend locally
   - [ ] Document the frontend

**Phase 4**: Integrate the API with the Frontend and test it on AWS.
   - [ ] Integrate the API with the frontend
   - [ ] Test the API and frontend on AWS
   - [ ] Document the integration

**Phase 5**: Finalize the project

[//]: # (   - [ ] Write a final report)

[//]: # (   - [ ] Finalize the documentation)

[//]: # (   - [ ] Finalize the tests)

[//]: # (   - [ ] Finalize the code)

### Current Status
Phase 1 is largely complete. There will be ongoing enhancements to the API as the project progresses as well improvements made to project dependencies. You can view the full code for this section in the [file_transfer_api](file_transfer_api/) directory