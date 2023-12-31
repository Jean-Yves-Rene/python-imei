from flask import Flask, render_template, request, jsonify
from warranty import get_current_warranty
from warranty import is_valid_imei
from waitress import serve
from SKU_designation import get_product_description
import json


app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/warranty')
def get_warranty():
    imei = request.args.get('imei')
    # Check for empty strings or string with only spaces
    imei_to_check = imei
    if is_valid_imei(imei_to_check):
        print(f"{imei_to_check} is a valid IMEI.")
    else:
        print(f"{imei_to_check} is not a valid IMEI.")
    # Assuming get_current_warranty returns a response object
    warranty_data = get_current_warranty(imei)

    # IMEI is not found by API
    data = json.loads(warranty_data.text)
    if data['success'] == False:
       return render_template('imei-not-found.html')  
    
    

    # Check if the request was successful (status code 200)
    if warranty_data.status_code == 200:
        # Load the JSON data
        # response_json = warranty_data.json()
        # Load the JSON data
        data = json.loads(warranty_data.text)
        sku_value = data['data']['device']['sku']
    # Get the product description based on the SKU
        result = get_product_description(sku_value)
        print(f"Description: {result}")  # Print the result for debugging purposes
        print(sku_value)

        return render_template(
            "warranty.html",
            Description_value = result,
            sku_value = sku_value,
            product_line_id_value = data['data']['device']['product_line_id'],
            product_line_value = data['data']['device']['product_line'],
            imei_value = data['data']['device']['imei'],
            serial_number_value = data['data']['device']['serial_number'],
            warranty_status_value = data['data']['device']['warranty_status'],
            warranty_end_date_value = data['data']['device']['warranty_end_date'],
            product_line_authorization_value = data['data']['device']['product_line_authorization'],
        )
    else:
        # Return an error message if the request was not successful
        return render_template("error.html", error=f"Request failed with status code: {warranty_data.status_code}")

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
