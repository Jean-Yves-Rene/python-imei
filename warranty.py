from dotenv import load_dotenv
from pprint import pprint
import requests
import os
import json

# Load environment variables
load_dotenv()

# Get header values from environment variables
api_key = os.getenv('API_KEY')
session_id = os.getenv('SESSION_ID')
route_1 = os.getenv('ROUTE_1')
route_2 = os.getenv('ROUTE_2')

payload = "{\"query\":\"\",\"variables\":{}}"

# Construct headers dictionary
headers = {
    'x-api-key': api_key,
    'Cookie': f'ASP.NET_SessionId={session_id}; X-Oracle-BMC-LBS-Route={route_1}; X-Oracle-BMC-LBS-Route={route_2}',
    'Content-Type': 'application/json'
}

def get_current_warranty(imei):
    url = f'https://google.servicecentral.com/sctapi/device/{imei}'
    response = requests.get(url, headers=headers, data=payload)
    return response

def is_valid_imei(imei):
    # Check if the IMEI is a string, 15 digits long, and consists only of digits
    return isinstance(imei, str) and len(imei) == 15 and imei.isdigit()

if __name__ == "__main__":
    print('\n*** Get Warranty Details for IMEI ***\n')

    imei = input("\nPlease enter an IMEI number 15 digits: ")

    if is_valid_imei(imei):
        print(f"{imei} is a valid IMEI.")
        warranty_data = get_current_warranty(imei)

        if warranty_data.status_code == 200:
            try:
                data = warranty_data.json()
                device_data = data.get('data', {}).get('device', {})

                sku_value = device_data.get('sku', 'N/A')
                product_line_id_value = device_data.get('product_line_id', 'N/A')
                product_line_value = device_data.get('product_line', 'N/A')
                imei_value = device_data.get('imei', 'N/A')
                serial_number_value = device_data.get('serial_number', 'N/A')
                warranty_status_value = device_data.get('warranty_status', 'N/A')
                warranty_end_date_value = device_data.get('warranty_end_date', 'N/A')
                product_line_authorization_value = device_data.get('product_line_authorization', 'N/A')

                # 'notes' can be a list, so handle it appropriately
                notes = device_data.get('notes', [])
                note_text = notes[0].get('note_text', 'No notes available') if notes else 'No notes available'

                # Print the details
                print(f'sku: {sku_value}')
                print(f'product_line_id: {product_line_id_value}')
                print(f'product_line: {product_line_value}')
                print(f'imei: {imei_value}')
                print(f'serial_number: {serial_number_value}')
                print(f'warranty_status: {warranty_status_value}')
                print(f'warranty_end_date: {warranty_end_date_value}')
                print(f'product_line_authorization: {product_line_authorization_value}')
                print(f'note_text: {note_text}')

            except json.JSONDecodeError:
                print("Error decoding JSON response")
            except (TypeError, KeyError) as e:
                print(f"Error processing response: {e}")
        else:
            print(f"Failed to fetch data. HTTP Status code: {warranty_data.status_code}")
    else:
        print(f"{imei} is not a valid IMEI.")
