from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosResourceExistsError
from azure.cosmos.partition_key import PartitionKey
import config as config

# Replace with your Cosmos DB connection details
HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']

# Initialize Cosmos DB client
client = CosmosClient(HOST, MASTER_KEY)

# Database and container setup
DATABASE_NAME = "Productdemo"
CONTAINER_NAME = "Products"

def create_database(database_name):
    try:
        database = client.create_database(id=database_name)
        print('Database created'.format(database_name))

    except CosmosResourceExistsError:
        database = client.get_database_client(database_name)
        print('Database was found'.format(database_name))

    return database

def create_container(database, container_name):
    try:
        container = database.create_container(id=container_name, partition_key=PartitionKey(path='/id'))
        print('Container created'.format(container_name))

    except CosmosResourceExistsError:
        container = database.get_container_client(container_name)
        print('Container was found'.format(container_name))

    return container

if __name__ == '__main__':
    database = create_database(DATABASE_NAME)
    container = create_container(database, CONTAINER_NAME)
    print("Container setup complete")
