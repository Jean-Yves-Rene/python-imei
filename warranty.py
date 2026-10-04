from dotenv import load_dotenv
from pprint import pprint
import requests
import os
import json
import re


# =========================================
# LOAD ENVIRONMENT VARIABLES
# =========================================

load_dotenv()


# =========================================
# GET HEADER VALUES FROM ENVIRONMENT
# =========================================

api_key = os.getenv('API_KEY')
session_id = os.getenv('SESSION_ID')
route_1 = os.getenv('ROUTE_1')
route_2 = os.getenv('ROUTE_2')


# =========================================
# PAYLOAD
# =========================================

payload = "{\"query\":\"\",\"variables\":{}}"


# =========================================
# CONSTRUCT HEADERS
# =========================================

headers = {
    'x-api-key': api_key,
    'Cookie': f'ASP.NET_SessionId={session_id}; X-Oracle-BMC-LBS-Route={route_1}; X-Oracle-BMC-LBS-Route={route_2}',
    'Content-Type': 'application/json'
}


# =========================================
# SNC VALIDATION
# =========================================

def is_valid_snc(snc):

    """
    Validate SNC / Claim Number.

    Required format:

        SNC696333

    Format:
        SNC + exactly 6 digits
    """

    if not isinstance(snc, str):
        return False

    snc = snc.strip().upper()

    return bool(re.fullmatch(r'SNC\d{6}', snc))


# =========================================
# GET SNC CLAIM
# =========================================

def get_snc_claim(snc):

    snc = snc.strip().upper()

    if not is_valid_snc(snc):
        raise ValueError(
            "Invalid SNC format. Required format: SNC696333"
        )

    url = f'https://google.servicecentral.com/sctapi/google-claims/{snc}'

    response = requests.get(
        url,
        headers=headers
    )

    return response


# =========================================
# GET CURRENT WARRANTY
# =========================================

def get_current_warranty(imei):

    url = f'https://google.servicecentral.com/sctapi/device/{imei}'

    response = requests.get(
        url,
        headers=headers,
        data=payload
    )

    return response


# =========================================
# IMEI VALIDATION
# =========================================

def is_valid_imei(imei):

    # Check if the IMEI is a string,
    # 15 digits long, and consists only of digits

    return (
        isinstance(imei, str)
        and len(imei) == 15
        and imei.isdigit()
    )


# =========================================
# TEST
# =========================================

if __name__ == "__main__":

    print('\n*** Google SCT API Test ***\n')

    print('1. Warranty Check')
    print('2. SNC Claim Check')

    choice = input('\nSelect option: ').strip()


    # =====================================
    # WARRANTY TEST
    # =====================================

    if choice == "1":

        print('\n*** Get Warranty Details for IMEI ***\n')

        imei = input(
            "\nPlease enter an IMEI number 15 digits: "
        )


        if is_valid_imei(imei):

            print(f"{imei} is a valid IMEI.")

            warranty_data = get_current_warranty(imei)


            if warranty_data.status_code == 200:

                try:

                    data = warranty_data.json()
                    device_data = data.get('data', {}).get('device', {})

                    sku_value = device_data.get('sku', 'N/A')
                    product_line_id_value = device_data.get(
                        'product_line_id',
                        'N/A'
                    )
                    product_line_value = device_data.get(
                        'product_line',
                        'N/A'
                    )
                    imei_value = device_data.get(
                        'imei',
                        'N/A'
                    )
                    serial_number_value = device_data.get(
                        'serial_number',
                        'N/A'
                    )
                    warranty_status_value = device_data.get(
                        'warranty_status',
                        'N/A'
                    )
                    warranty_end_date_value = device_data.get(
                        'warranty_end_date',
                        'N/A'
                    )
                    product_line_authorization_value = device_data.get(
                        'product_line_authorization',
                        'N/A'
                    )


                    # 'notes' can be a list,
                    # so handle it appropriately

                    notes = device_data.get('notes', [])

                    note_text = (
                        notes[0].get(
                            'note_text',
                            'No notes available'
                        )
                        if notes
                        else 'No notes available'
                    )


                    # =================================
                    # PRINT THE DETAILS
                    # =================================

                    print(f'sku: {sku_value}')

                    print(
                        f'product_line_id: '
                        f'{product_line_id_value}'
                    )

                    print(
                        f'product_line: '
                        f'{product_line_value}'
                    )

                    print(
                        f'imei: '
                        f'{imei_value}'
                    )

                    print(
                        f'serial_number: '
                        f'{serial_number_value}'
                    )

                    print(
                        f'warranty_status: '
                        f'{warranty_status_value}'
                    )

                    print(
                        f'warranty_end_date: '
                        f'{warranty_end_date_value}'
                    )

                    print(
                        f'product_line_authorization: '
                        f'{product_line_authorization_value}'
                    )

                    print(
                        f'note_text: '
                        f'{note_text}'
                    )


                except json.JSONDecodeError:

                    print(
                        "Error decoding JSON response"
                    )


                except (TypeError, KeyError) as e:

                    print(
                        f"Error processing response: {e}"
                    )


            else:

                print(
                    f"Failed to fetch data. "
                    f"HTTP Status code: "
                    f"{warranty_data.status_code}"
                )


        else:

            print(
                f"{imei} is not a valid IMEI."
            )


    # =====================================
    # SNC TEST
    # =====================================

    elif choice == "2":

        print('\n*** Google SCT API - SNC Claim ***\n')

        snc = input(
            "Please enter an SNC claim number "
            "(example SNC696333): "
        ).strip().upper()


        # =================================
        # VALIDATE SNC
        # =================================

        if not is_valid_snc(snc):

            print(
                f"\n{snc} is not a valid SNC claim number."
            )

            print(
                "Required format: SNC696333"
            )


        else:

            print(
                f"\n{snc} is a valid SNC claim number."
            )


            try:

                claim_response = get_snc_claim(snc)


                # =================================
                # API RESPONSE
                # =================================

                if claim_response.status_code == 200:

                    try:

                        data = claim_response.json()

                        print(
                            "\n*** Claim Information ***\n"
                        )

                        pprint(data)


                    except json.JSONDecodeError:

                        print(
                            "Error decoding JSON response."
                        )


                else:

                    print(
                        f"Failed to fetch claim data. "
                        f"HTTP Status code: "
                        f"{claim_response.status_code}"
                    )

                    print(
                        claim_response.text
                    )


            except requests.RequestException as e:

                print(
                    f"API request failed: {e}"
                )


            except ValueError as e:

                print(e)


    # =====================================
    # INVALID MENU SELECTION
    # =====================================

    else:

        print(
            "\nInvalid selection."
        )