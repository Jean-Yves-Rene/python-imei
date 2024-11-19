def create_product_dict(product_data):
    product_dict = {}

    # Split the data into lines and process each line
    for line in product_data.strip().split('\n'):
        # Skip empty lines
        if not line.strip():
            continue
        try:
            # Split each line into SKU and product information
            sku, info = line.split('\t', 1)

            # If SKU is not in the dictionary, add it with the product information
            if sku not in product_dict:
                # Split the product information and add each piece separately to the list
                product_dict[sku] = info.split('\t')
            else:
                # If SKU is already in the dictionary, append each piece of information separately
                product_dict[sku].extend(info.split('\t'))
        except ValueError:
            # Handle malformed lines gracefully
            print(f"Skipping malformed line: {repr(line)}")
    return product_dict

