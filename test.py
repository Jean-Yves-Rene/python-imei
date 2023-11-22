import requests
import json

url = "https://google.servicecentral.com/sctapi/device/1A121FDEE0072Z"

payload = "{\"query\":\"\",\"variables\":{}}"
headers = {
  'x-api-key': 'c2JldWstYXBpQHNlcnZpY2VjZW50cmFsLmNvbTpmUks0UF4hN2Z9elg6Q0VDQTM2RDZERjI1Qjc3MkUwNTNEODEwMDAwQTRDODc=',
  'Cookie': 'ASP.NET_SessionId=b2widazbiw51inixwuh4o2cp; X-Oracle-BMC-LBS-Route=08fcb970a6df91d4a0484e18bd5e2cc37730f0a9; X-Oracle-BMC-LBS-Route=66fa2725a70221c5af25dedf62704d05050dcd39',
  'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
# Load the JSON data
data = json.loads(response.text)

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
print(f'sku: {sku_value}')
print(f'product_line_id: {product_line_id_value}')
print(f'product_line: {product_line_value}')
print(f'imei: {imei_value}')
print(f'serial_number: {serial_number_value}')
print(f'warranty_status: {warranty_status_value}')
print(f'warranty_end_date: {warranty_end_date_value}')
print(f'product_line_authorization: {product_line_authorization_value}')