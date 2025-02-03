from pymongo import MongoClient
import os

# Load MongoDB credentials
mongodb_username = os.getenv('MONGODB_USERNAME')
mongodb_password = os.getenv('MONGODB_PASSWORD')
mongodb_ip = os.getenv('MONGODB_IP')
mongodb_auth_source = os.getenv('MONGODB_AUTH_SOURCE')

# MongoDB Connection
uri = f"mongodb://{mongodb_username}:{mongodb_password}@{mongodb_ip}/?authSource={mongodb_auth_source}"
mongo_client = MongoClient(uri)
db = mongo_client["local"]  # Change if using another database
collection = db["SKU_List_GG"]  # Change to your actual collection name

def get_product_description(sku_value):
    print(collection.find_one())  # See if connection is working

    """Fetch SKU description from MongoDB."""
    product = collection.find_one({"sku": sku_value})
    
    if product:
        return product.get("designation", "No description available")
    else:
        return f"Description for SKU {sku_value} not found."
