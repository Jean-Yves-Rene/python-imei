from flask import Flask, render_template, request, jsonify
from warranty import get_current_warranty, is_valid_imei
from waitress import serve
from SKU_designation import get_product_description
import json
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/warranty')
def get_warranty():
    imei = request.args.get('imei')
    
    if not is_valid_imei(imei):
        return render_template("imei-not-found.html")

    try:
        # Fetch warranty data
        warranty_data = get_current_warranty(imei)

        # Check if the request was successful
        if warranty_data.status_code == 200:
            data = json.loads(warranty_data.text)
            
            if not data.get('success', True):
                return render_template('imei-not-found.html')

            device_data = data.get('data', {}).get('device', {})

            if not device_data:
                return render_template('imei-not-found.html')

            sku_value = device_data.get('sku', 'N/A')

            # Ensure the sku_value is long enough before slicing
            if len(sku_value) >= 13 and sku_value[8:13] == "EU-RA":
                new_sku_value = sku_value.replace("EU-RA", "GB")
            elif len(sku_value) >= 13 and sku_value[8:13] == "GB-RA":
                new_sku_value = sku_value.replace("GB-RA", "GB")
            else:
                new_sku_value = sku_value

            result = get_product_description(new_sku_value)

            notes = device_data.get('notes', [])
            note_text = notes[0].get('note_text', 'No notes available') if notes else 'No notes available'

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
                note_text=note_text,
            )
        else:
            logging.error(f"Request failed with status code: {warranty_data.status_code}")
            data = json.loads(warranty_data.text)
            message = data.get("message", "No message available")
            return render_template("error.html", error=f"Request failed with status code: {warranty_data.status_code}. Message: {message}")
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return render_template("error.html", error="An unexpected error occurred while processing your request.")

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
