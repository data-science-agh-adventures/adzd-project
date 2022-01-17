from azure.cosmos import CosmosClient
import os

url = os.environ['ACCOUNT_URI']
key = os.environ['ACCOUNT_KEY']
client = CosmosClient(url, credential=key)
database_name = 'testDatabase'
database = client.get_database_client(database_name)
container_name = 'products'
container = database.get_container_client(container_name)

container.upsert_item({
    # 'id': 'item{0}'.format(i),  # if not set, then Cosmos will set a random UUID
    'productName': 'Widget',
    'productModel': 'Model Test'
    })