from dotenv import load_dotenv
from pprint import pprint
import requests
import os
import json

load_dotenv()

# Get header values from environment variables
api_key = os.getenv('API_KEY')
session_id = os.getenv('SESSION_ID')
route_1 = os.getenv('ROUTE_1')
route_2 = os.getenv('ROUTE_2')
#url = "https://google.servicecentral.com/sctapi/device/1A121FDEE0072Z"
payload = "{\"query\":\"\",\"variables\":{}}"
# Construct headers dictionary

headers ={
    'x-api-key': api_key,
    'Cookie': f'ASP.NET_SessionId={session_id}; X-Oracle-BMC-LBS-Route={route_1}; X-Oracle-BMC-LBS-Route={route_2}',
    'Content-Type': 'application/json'
}
#print(f'API Key: {api_key}')
#print(f'Session ID: {session_id}')
#print(f'Route 1: {route_1}')
#print(f'Route 2: {route_2}')


def get_current_warranty(imei):

    url = f'https://google.servicecentral.com/sctapi/device/{imei}'

    warranty_data = requests.request("GET", url, headers=headers, data=payload)

    return warranty_data

def is_valid_imei(imei):
    # Check if the IMEI is a string
    if not isinstance(imei, str):
        return False

    # Check if the IMEI is 15 digits long
    if len(imei) != 15:
        return False

    # Check if the IMEI consists only of digits
    if not imei.isdigit():
        return False

    # If all checks pass, the IMEI is valid
    return True

if __name__ == "__main__":
    print('\n*** Get Warranty Details for IMEI ***\n')

    imei = input("\nPlease enter an IMEI number 15 digits: ")

    # Check for empty strings or string with only spaces
    imei_to_check = imei
    if is_valid_imei(imei_to_check):
        print(f"{imei_to_check} is a valid IMEI.")
    else:
        print(f"{imei_to_check} is not a valid IMEI.")

    warranty_data = get_current_warranty(imei)

    print("\n")
   # Assuming warranty_data is a requests.Response object
    #for line in warranty_data.text.split('\n'):
        #print(line)
    print(warranty_data.text)
    # Load the JSON data
    data = json.loads(warranty_data.text)

    # Access the SKU value
    sku_value = data['data']['device']['sku']
    product_line_id_value = data['data']['device']['product_line_id']
    product_line_value = data['data']['device']['product_line']
    imei_value = data['data']['device']['imei']
    serial_number_value = data['data']['device']['serial_number']
    warranty_status_value = data['data']['device']['warranty_status']
    warranty_end_date_value = data['data']['device']['warranty_end_date']
    product_line_authorization_value = data['data']['device']['product_line_authorization']


    # Print the SKU
    # print(f'sku: {sku_value}')
    # print(f'product_line_id: {product_line_id_value}')
    # print(f'product_line: {product_line_value}')
    # print(f'imei: {imei_value}')
    # print(f'serial_number: {serial_number_value}')
    # print(f'warranty_status: {warranty_status_value}')
    # print(f'warranty_end_date: {warranty_end_date_value}')
    # print(f'product_line_authorization: {product_line_authorization_value}')

