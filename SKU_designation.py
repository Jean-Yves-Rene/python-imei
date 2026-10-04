from pymongo import MongoClient
import os


# Load MongoDB credentials
mongodb_username = os.getenv('MONGODB_USERNAME')
mongodb_password = os.getenv('MONGODB_PASSWORD')
mongodb_ip = os.getenv('MONGODB_IP')
mongodb_auth_source = os.getenv('MONGODB_AUTH_SOURCE')


# MongoDB Connection
uri = (
    f"mongodb://{mongodb_username}:"
    f"{mongodb_password}@{mongodb_ip}/"
    f"?authSource={mongodb_auth_source}"
)

mongo_client = MongoClient(uri)

db = mongo_client["local"]

collection = db["SKU_List_GG"]


def get_product_description(sku_value):

    """Fetch SKU description from MongoDB."""

    product = collection.find_one({
        "sku": sku_value
    })

    if product:

        return product.get(
            "designation",
            "No description available"
        )

    else:

        return (
            f"Description for SKU "
            f"{sku_value} not found."
        )
