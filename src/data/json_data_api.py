import requests
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.exceptions import CosmosResourceExistsError
import config as config

# Cosmos DB connection details
HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
DATABASE_ID = config.settings['database_id']
CONTAINER_ID = config.settings['container_id']

client = CosmosClient(HOST, MASTER_KEY)
database = client.get_database_client(DATABASE_ID)
container = database.get_container_client(CONTAINER_ID)

# Loop through product IDs from 1 to 100
for product_id in range(1, 101):
    # Construct the URL dynamically
    URL = f"https://dummyjson.com/products/{product_id}"

    # Fetch data from the API
    response = requests.get(URL)

    # Ensure the API call was successful
    if response.status_code == 200:
        product_data = response.json()
        print(f"Product {product_id} fetched successfully!")
        
        # Add or modify any other fields as necessary (like partition key)
        product_data["id"] = str(product_data.get("id", "Unknown"))

        try:
            # Insert the item into Cosmos DB container
            container.create_item(body=product_data)
            print(f"Product {product_id} inserted successfully!")
        except CosmosResourceExistsError:
            print(f"Product {product_id} already exists!")

    else:
        print(f"Failed to fetch product {product_id}: {response.status_code}")