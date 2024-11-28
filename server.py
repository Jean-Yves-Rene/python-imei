from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from functools import wraps
from warranty import get_current_warranty, is_valid_imei
from waitress import serve
from SKU_designation import get_product_description
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import timedelta
from datetime import datetime
from pymongo import MongoClient
import pymongo
import logging
import os
import bcrypt
import json

app = Flask(__name__)

# # Configure Flask-Limiter
# limiter = Limiter(
#     get_remote_address,
#     app=app,
#     default_limits=["200 per day", "50 per hour"]  # Global rate limits
# )

# Configure logging
logging.basicConfig(level=logging.INFO)

MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")

# Environment variables for credentials
usernamestored = os.getenv('USERNAMELOGIN')
stored_hashed_password = os.getenv('PASSWORDHASHED')  # Securely hashed password

# Secret key for session management
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'mysecretkey')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)  # 5-minute session timeout

# Use credentials to connect to MongoDB
uri = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@cluster0.zvtjbni.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)

db = client["Google"]  # Replace "your_database_name" with your actual database name
collection = db["ImeiWarrantyCheck"]  # Replace "your_collection_name" with your actual collection name

try:
    # Connect to MongoDB
    #client = pymongo.MongoClient(uri)

    # Check if connection is successful
    db_names = client.list_database_names()
    print("Connected to MongoDB")
    print("Available databases:")
    for db_name in db_names:
        print(db_name)

except pymongo.errors.ConnectionFailure as e:
    print("Could not connect to MongoDB:", e)
# Function to get current date and time
def get_current_date():
    return datetime.now()

# Login decorator to protect routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))  # Redirect to login if session expired
        return f(*args, **kwargs)
    return decorated_function

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
    return redirect(url_for('login'))  # Redirect to login

# Login route with rate limiting
@app.route('/login', methods=['GET', 'POST'])
#@limiter.limit("5 per minute")  # Specific rate limit for login
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
       
        if not stored_hashed_password:
            logging.error("Environment variable 'PASSWORDHASHED' is not set.")
            return "Server misconfiguration. Please contact the administrator.", 500

        # Validate credentials
        try:
            if username == usernamestored and bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                session['username'] = username
                session.permanent = True  # Enable session timeout
                logging.info(f"User {username} logged in successfully.")
                return redirect(url_for('dashboard'))
            else:
                logging.warning(f"Failed login attempt for username: {username}")
                return render_template('errorlogin.html', error="Invalid credentials.")
        except Exception as e:
            logging.error(f"Login error: {e}")
            return "An error occurred during login. Please try again later.", 500

    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    session.clear()  # Clear the entire session
    session.pop('username', None)
    logging.info("User logged out.")
    return redirect(url_for('login'))

# Dashboard route
@app.route('/dashboard')
@login_required
def dashboard():
    username = session.get('username')  # Get username from session
    if not username:
        flash("Session expired. Please log in again.", "danger")
        return redirect(url_for('login'))
    else:
        return render_template('index.html', username=session['username'])

# Warranty route
@app.route('/warranty')
@login_required
def warranty():
    username = session.get('username')  # Get username from session
    if not username:
        flash("Session expired. Please log in again.", "danger")
        return redirect(url_for('login'))
    imei = request.args.get('imei')

    try:
        warranty_data = get_current_warranty(imei)

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
            collection.insert_one(data)
            print(imei)

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
        else:
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
