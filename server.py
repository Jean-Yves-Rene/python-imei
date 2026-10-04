from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session,
    redirect,
    url_for,
    flash
)

from functools import wraps

from warranty import (
    get_current_warranty,
    get_snc_claim,
    is_valid_imei
)

from waitress import serve
from dotenv import load_dotenv

from SKU_designation import get_product_description

from datetime import timedelta
from datetime import datetime

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

import pymongo
import logging
import os
import json


# =========================================================
# Create Flask application
# =========================================================

app = Flask(__name__)


# =========================================================
# Configure logging
# =========================================================

logging.basicConfig(
    level=logging.INFO
)


# =========================================================
# Load environment variables
# =========================================================

load_dotenv()


# =========================================================
# MongoDB environment variables
# =========================================================

mongodb_username = os.getenv(
    'MONGODB_USERNAME'
)

mongodb_password = os.getenv(
    'MONGODB_PASSWORD'
)

mongodb_ip = os.getenv(
    'MONGODB_IP'
)

mongodb_auth_source = os.getenv(
    'MONGODB_AUTH_SOURCE'
)


# =========================================================
# Server environment variables
# =========================================================

IP_SERVER_PORT = os.getenv(
    'IP_SERVER_PORT',
    '127.0.0.1'
)

PORT_SERVER = int(
    os.getenv(
        'PORT_SERVER',
        '5001'
    )
)


# =========================================================
# Flask secret key / session
# =========================================================

app.secret_key = os.getenv(
    'FLASK_SECRET_KEY',
    'mysecretkey'
)

app.config[
    'PERMANENT_SESSION_LIFETIME'
] = timedelta(
    minutes=60
)


# =========================================================
# MongoDB connection
# =========================================================

uri = (
    f"mongodb://{mongodb_username}:"
    f"{mongodb_password}@{mongodb_ip}/"
    f"?authSource={mongodb_auth_source}"
)

mongo_client = MongoClient(
    uri
)


# =========================================================
# MongoDB database
# =========================================================

db = mongo_client["local"]


# =========================================================
# Existing IMEI collection
# =========================================================

collection = db[
    "Google_Warranty_Check"
]


# =========================================================
# Warranty comments collection
# =========================================================

warranty_comments = db[
    "warranty_comments"
]


# =========================================================
# SNC checker collection
# =========================================================

snc_collection = db[
    "Google_SNC_Check"
]


# =========================================================
# Get current date and time
# =========================================================

def get_current_date():

    return datetime.now()


# =========================================================
# Disable browser caching
# =========================================================

@app.after_request
def add_no_cache_headers(response):

    response.headers["Cache-Control"] = (
        "no-store, no-cache, must-revalidate, "
        "post-check=0, pre-check=0, max-age=0"
    )

    response.headers["Pragma"] = "no-cache"

    response.headers["Expires"] = "0"

    return response


# =========================================================
# Rate limit error handler
# =========================================================

@app.errorhandler(429)
def ratelimit_error(e):

    return jsonify(
        error=(
            "Too many requests. "
            "Please try again later."
        )
    ), 429


# =========================================================
# 400 Error
# =========================================================

@app.errorhandler(400)
def bad_request_error(e):

    return render_template(
        'index.html'
    ), 400


# =========================================================
# 404 Error
# =========================================================

@app.errorhandler(404)
def not_found_error(e):

    return render_template(
        'index.html'
    ), 404


# =========================================================
# Home route
# =========================================================

@app.route('/')
def home():

    return render_template(
        'index.html'
    )


# =========================================================
# SNC CHECKER
# =========================================================

@app.route(
    '/snc-checker',
    methods=['GET', 'POST']
)
def snc_checker():

    result = None

    error = None


    # =====================================================
    # Only process SNC when the form is submitted
    # =====================================================

    if request.method == 'POST':

        snc = request.form.get(
            'snc',
            ''
        ).strip()


        # =================================================
        # Validate SNC input
        # =================================================

        if not snc:

            error = (
                "Please enter an "
                "SNC / claim number."
            )


        else:

            try:

                # =============================================
                # Call SNC API
                # =============================================

                response = get_snc_claim(
                    snc
                )


                logging.info(
                    f"SNC API response: "
                    f"{response.status_code} - "
                    f"{response.text}"
                )


                # =============================================
                # Successful API response
                # =============================================

                if response.status_code == 200:

                    data = response.json()


                    # =========================================
                    # API says success
                    # =========================================

                    if data.get('success'):

                        result = data.get(
                            'data',
                            {}
                        )


                        # =====================================
                        # Save SNC lookup to MongoDB
                        # =====================================

                        snc_entry = {

                            "snc": snc,

                            "ticket_id": result.get(
                                "ticket_id"
                            ),

                            "status": result.get(
                                "status"
                            ),

                            "status_timestamp": result.get(
                                "status_timestamp"
                            ),

                            "equipment": result.get(
                                "equipment",
                                {}
                            ),

                            "equipment_sku": result.get(
                                "equipment_sku"
                            ),

                            "product_line": result.get(
                                "product_line"
                            ),

                            "asp_tier": result.get(
                                "asp_tier"
                            ),

                            "asp_level": result.get(
                                "asp_level"
                            ),

                            "authorization_code": result.get(
                                "authorization_code"
                            ),

                            "t_codes": result.get(
                                "t_codes",
                                []
                            ),

                            "date_checked": get_current_date().strftime(
                                "%Y-%m-%dT%H:%M"
                            )
                        }


                        # =====================================
                        # Insert into MongoDB
                        # =====================================

                        snc_collection.insert_one(
                            snc_entry
                        )


                    # =========================================
                    # API returned success = false
                    # =========================================

                    else:

                        error = data.get(
                            'message',
                            'SNC not found.'
                        )


                # =============================================
                # API returned an HTTP error
                # =============================================

                else:

                    error = (
                        f"SNC lookup failed. "
                        f"HTTP status: "
                        f"{response.status_code}"
                    )


            except Exception as e:

                logging.error(
                    f"SNC lookup error: {e}"
                )

                error = (
                    "An unexpected error occurred "
                    "while checking the SNC."
                )


    # =====================================================
    # Display SNC page
    # =====================================================

    return render_template(
        'snc-checker.html',
        result=result,
        error=error
    )


# =========================================================
# WARRANTY ROUTE
# =========================================================

@app.route('/warranty')
def warranty():

    imei = request.args.get(
        'imei'
    )

    if not imei:

        return render_template(
            'index.html'
        )


    try:

        # =====================================================
        # Get warranty information from warranty API
        # =====================================================

        warranty_data = get_current_warranty(
            imei
        )


        logging.info(
            f"Warranty API response: "
            f"{warranty_data.status_code} - "
            f"{warranty_data.text}"
        )


        # =====================================================
        # Successful API response
        # =====================================================

        if warranty_data.status_code == 200:

            data = json.loads(
                warranty_data.text
            )


            # =================================================
            # API says no data found
            # =================================================

            if not data.get(
                'success',
                True
            ):

                current_date = (
                    get_current_date()
                    .strftime(
                        "%Y-%m-%dT%H:%M"
                    )
                )


                no_data_entry = {

                    "imei": imei,

                    "sku_value": "N/A",

                    "designation": "No Data Found",

                    "date_added": current_date
                }


                collection.insert_one(
                    no_data_entry
                )


                return render_template(
                    'imei-not-found.html'
                )


            # =================================================
            # Get device data
            # =================================================

            device_data = data.get(
                'data',
                {}
            ).get(
                'device',
                {}
            )


            if not device_data:

                return render_template(
                    'imei-not-found.html'
                )


            # =================================================
            # Get SKU
            #
            # Keep SKU exactly as returned by the API.
            # =================================================

            sku_value = device_data.get(
                'sku',
                'N/A'
            )

            sku_value = str(
                sku_value
            )


            print(
                "SKU returned by API:",
                sku_value
            )


            # =================================================
            # Get product description
            # =================================================

            result = get_product_description(
                sku_value
            )


            print(
                "Product description:",
                result
            )


            if (
                isinstance(result, list)
                and len(result) == 1
            ):

                result = result[0]


            # =================================================
            # Save IMEI lookup to MongoDB
            # =================================================

            current_date = (
                get_current_date()
                .strftime(
                    "%Y-%m-%dT%H:%M"
                )
            )


            imei_entry = {

                "imei": imei,

                "sku_value": sku_value,

                "designation": result,

                "date_added": current_date
            }


            collection.insert_one(
                imei_entry
            )


            print(
                "IMEI:",
                imei
            )


            # =================================================
            # Get notes from warranty API
            # =================================================

            notes = device_data.get(
                'notes',
                []
            )


            note_text = "No notes available"


            if notes:

                if isinstance(
                    notes,
                    list
                ):

                    if len(notes) > 0:

                        first_note = notes[0]

                        if isinstance(
                            first_note,
                            dict
                        ):

                            note_text = first_note.get(
                                'note_text',
                                'No notes available'
                            )

                        elif isinstance(
                            first_note,
                            str
                        ):

                            note_text = first_note


                elif isinstance(
                    notes,
                    dict
                ):

                    note_text = notes.get(
                        'note_text',
                        'No notes available'
                    )


                elif isinstance(
                    notes,
                    str
                ):

                    note_text = notes


            if not note_text:

                note_text = "No notes available"


            # =================================================
            # Log notes for troubleshooting
            # =================================================

            logging.info(
                f"Warranty API notes: {notes}"
            )

            logging.info(
                f"Note displayed on page: {note_text}"
            )


            # =================================================
            # Get warranty comments from MongoDB
            # =================================================

            comments_doc = (
                warranty_comments.find_one({
                    "type": "warranty_notice",
                    "active": True
                })
            )


            warranty_intro = ""

            warranty_comments_list = []

            warranty_action = ""

            warranty_updates = []


            if comments_doc:

                # ---------------------------------------------
                # Introduction
                # ---------------------------------------------

                warranty_intro = comments_doc.get(
                    "intro",
                    ""
                )


                # ---------------------------------------------
                # Final action
                # ---------------------------------------------

                warranty_action = comments_doc.get(
                    "action",
                    ""
                )


                # ---------------------------------------------
                # Warning comments
                # ---------------------------------------------

                warranty_comments_list = sorted(
                    comments_doc.get(
                        "comments",
                        []
                    ),
                    key=lambda x: x.get(
                        "sort_order",
                        999
                    )
                )


                # ---------------------------------------------
                # Warranty updates
                # ---------------------------------------------

                warranty_updates = sorted(
                    comments_doc.get(
                        "updates",
                        []
                    ),
                    key=lambda x: x.get(
                        "sort_order",
                        999
                    )
                )


            # =================================================
            # Render warranty page
            # =================================================

            return render_template(

                "warranty.html",

                Description_value=result,

                sku_value=sku_value,

                product_line_id_value=device_data.get(
                    'product_line_id',
                    'N/A'
                ),

                product_line_value=device_data.get(
                    'product_line',
                    'N/A'
                ),

                imei_value=device_data.get(
                    'imei',
                    'N/A'
                ),

                serial_number_value=device_data.get(
                    'serial_number',
                    'N/A'
                ),

                warranty_status_value=device_data.get(
                    'warranty_status',
                    'N/A'
                ),

                warranty_end_date_value=device_data.get(
                    'warranty_end_date',
                    'N/A'
                ),

                product_line_authorization_value=device_data.get(
                    'product_line_authorization',
                    'N/A'
                ),

                note_text=note_text,

                warranty_intro=warranty_intro,

                warranty_comments=warranty_comments_list,

                warranty_action=warranty_action,

                warranty_updates=warranty_updates
            )


        # =====================================================
        # Warranty API returned an error
        # =====================================================

        else:

            logging.error(
                f"Warranty request failed with "
                f"status code: "
                f"{warranty_data.status_code}"
            )


            data = json.loads(
                warranty_data.text
            )


            message = data.get(
                "message",
                "No message available"
            )


            current_date = (
                get_current_date()
                .strftime(
                    "%Y-%m-%dT%H:%M"
                )
            )


            error_entry = {

                "imei": imei,

                "sku_value": "N/A",

                "designation": (
                    "Not Found or Invalid"
                ),

                "date_added": current_date,

                "status_code": (
                    warranty_data.status_code
                )
            }


            collection.insert_one(
                error_entry
            )


            return render_template(
                "errordatanotfound.html",
                error=(
                    f"Request failed with "
                    f"status code: "
                    f"{warranty_data.status_code}. "
                    f"Message: {message}"
                )
            )


    # =========================================================
    # Unexpected warranty error
    # =========================================================

    except Exception as e:

        logging.error(
            f"An error occurred in /warranty: {e}"
        )


        current_date = (
            get_current_date()
            .strftime(
                "%Y-%m-%dT%H:%M"
            )
        )


        error_entry = {

            "imei": imei,

            "sku_value": "N/A",

            "designation": "Error Occurred",

            "date_added": current_date,

            "status_code": 500
        }


        collection.insert_one(
            error_entry
        )


        return render_template(
            "errordatanotfound.html",
            error=(
                "An unexpected error occurred."
            )
        )


# =========================================================
# Start application
# =========================================================

if __name__ == "__main__":

    serve(
        app,
        host=IP_SERVER_PORT,
        port=PORT_SERVER
    )