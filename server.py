from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from functools import wraps
from warranty import get_current_warranty, is_valid_imei
from waitress import serve
from dotenv import load_dotenv
from SKU_designation import get_product_description
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import timedelta
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import pymongo
import logging
import os
import json

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv()

# Access environment variables
mongodb_username = os.getenv('MONGODB_USERNAME')
mongodb_password = os.getenv('MONGODB_PASSWORD')
mongodb_ip = os.getenv('MONGODB_IP')
mongodb_auth_source = os.getenv('MONGODB_AUTH_SOURCE')

# Secret key for session management
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'mysecretkey')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)  # 5-minute session timeout

# Construct the MongoDB URI using the loaded environment variables
uri = f"mongodb://{mongodb_username}:{mongodb_password}@{mongodb_ip}/?authSource={mongodb_auth_source}"
client = None

try:
    client = MongoClient(uri)
    # Check if connection is successful
    db_names = client.list_database_names()
    print("Connected to MongoDB")
    print("Available databases:")
    for db_name in db_names:
        print(db_name)
except ConnectionFailure as e:
    print("Could not connect to MongoDB:", e)
    client = None

collection = None

if client:
    db = client["local"]  # Replace with your actual database name
    collection = db["Google_Warranty_Check"]  # Replace with your actual collection name
else:
    collection = None # Ensure collection is None if client isn't connected
    logging.error("MongoDB client or collection is not initialized.")

# Function to get current date and time
def get_current_date():
    return datetime.now()

@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Rate limit error handler
@app.errorhandler(429)
def ratelimit_error(e):
    return jsonify(error="Too many requests. Please try again later."), 429

@app.errorhandler(400)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('index.html'), 400

@app.errorhandler(404)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('index.html'), 404

# Home route
@app.route('/')
def home():
    return render_template ('index.html')  

# Warranty route with rate limiting
@app.route('/warranty')
def warranty():
    imei = request.args.get('imei')

    try:
        warranty_data = get_current_warranty(imei)
        logging.info(f"Warranty API response: {warranty_data.status_code} - {warranty_data.text}")
         
        if warranty_data.status_code == 200:
            data = json.loads(warranty_data.text)

            if not data.get('success', True):
                return render_template('imei-not-found.html')

            device_data = data.get('data', {}).get('device', {})
            if not device_data:
                return render_template('imei-not-found.html')

            sku_value = device_data.get('sku', 'N/A')
            if len(sku_value) >= 13:
                if "EU-RA" in sku_value:
                    sku_value = sku_value.replace("EU-RA", "GB")
                elif "GB-RA" in sku_value:
                    sku_value = sku_value.replace("GB-RA", "GB")
            # Insert IMEI into MongoDB collection
            result = get_product_description(sku_value)
            print(result)
            if isinstance(result, list) and len(result) == 1:
                result = result[0]  # Extract the single value
            # Add current date to the data
            current_date = get_current_date().strftime("%Y-%m-%dT%H:%M")
            data = {
                "imei": imei,
                "sku_value": sku_value,
                "designation": result,
                "date_added": current_date  # Add date field,
                }
            if client is not None and collection is not None:
                try:
                    collection.insert_one(data)
                    logging.info(f"Inserted IMEI data into MongoDB: {data}")
                except Exception as db_error:
                    logging.error(f"Error inserting data into MongoDB: {db_error}")
                    return render_template("errordatanotfound.html", error="Database insertion failed.")
            else:
                return render_template("error.html", error="MongoDB client is not connected.")
        
            notes = device_data.get('notes', [{'note_text': 'No notes available'}])

            return render_template(
                "warranty.html",
                Description_value=result,
                sku_value=sku_value,
                product_line_id_value=device_data.get('product_line_id', 'N/A'),
                product_line_value=device_data.get('product_line', 'N/A'),
                imei_value=device_data.get('imei', 'N/A'),
                serial_number_value=device_data.get('serial_number', 'N/A'),
                warranty_status_value=device_data.get('warranty_status', 'N/A'),
                warranty_end_date_value=device_data.get('warranty_end_date', 'N/A'),
                product_line_authorization_value=device_data.get('product_line_authorization', 'N/A'),
                note_text=notes[0].get('note_text'),
            )
        elif warranty_data.status_code == 400 or warranty_data.status_code == 404 :
            logging.error(f"Warranty request failed with status code: {warranty_data.status_code}")
            data = json.loads(warranty_data.text)
            message = data.get("message", "No message available")
            return render_template("errordatanotfound.html", error=f"Request failed with status code: {warranty_data.status_code}. Message: {message}")
    except Exception as e:
            logging.error(f"An error occurred in /warranty: {e}")
            return render_template("errordatanotfound.html", error="An unexpected error occurred.")

@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
