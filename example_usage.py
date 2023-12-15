from client.fastapi_client import FastAPIClient

client = FastAPIClient()
response = client.get_file_metadata("1234")
print(response.json())