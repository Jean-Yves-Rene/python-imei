import utils


product_data = """
GA00681-UK	PIXEL 4 BLACK 128GB CORE UK
GA00681-US	PIXEL 4 BLACK 128GB FOREIGN (US)
GA01378-US	PIXEL 4 BLACK 128GB FOREIGN (US)
GA01187-UK	PIXEL 4 BLACK 64GB CORE UK
GA01187-DE	PIXEL 4 BLACK 64GB FOREIGN (DE)
GA01240-US	PIXEL 4 BLACK 64GB FOREIGN (US ATT)
GA01235-US	PIXEL 4 BLACK 64GB FOREIGN (US VZ)
GA01241-US	PIXEL 4 BLACK 64GB FOREIGN (US)
GA01187-US	PIXEL 4 BLACK 64GB FOREIGN (US)
GA01375-US	PIXEL 4 BLACK 64GB FOREIGN (US)
GA01192-UK	PIXEL 4 ORANGE 128GB CORE UK
GA01189-UK	PIXEL 4 ORANGE 64GB CORE UK
GA01191-UK	PIXEL 4 WHITE 128GB CORE UK
GA01267-US	PIXEL 4 CLEARLY WHITE 128GB FOREIGN US
GA01188-UK	PIXEL 4 WHITE 64GB CORE UK
GA01242-US	PIXEL 4 CLEARLY WHITE 64GB FOREIGN (US)
GA02099-EU	PIXEL 4A JUST BLACK 128GB CORE EU
GA02099-UK	PIXEL 4A BLACK 128GB CORE UK
GA02325-UK	PIXEL 4A JUST BLACK 128GB CORE UK DEMO
GA02099-US	PIXEL 4A BLACK 128GB FOREIGN
GA01738-US	PIXEL 4A BLACK 128GB FOREIGN
GA02099-FR	PIXEL 4A BLACK 128GB FOREIGN
GA02114-US	PIXEL 4A BLACK 128GB FOREIGN
GA02101-UK	PIXEL 4A BLUE 128GB CORE UK
GA02101-US	PIXEL 4A BLUE 128GB FOREIGN
GA01311-UK	PIXEL 4A 5G JUST BLACK 128GB CORE UK
GA02598-UK	PIXEL 4A 5G JUST BLACK 128GB CORE UK
GA02293-US	PIXEL 4A 5G JUST BLACK 128GB FOREIGN
GA01311-FR	PIXEL 4A 5G JUST BLACK 128GB FOREIGN
GA02290-US	PIXEL 4A 5G JUST BLACK 128GB FOREIGN
GA01311-DE	PIXEL 4A 5G JUST BLACK 128GB FOREIGN
GA02596-US	PIXEL 4A 5G JUST BLACK 128GB FOREIGN
GA02281-US	PIXEL 4A 5G JUST BLACK 128GB FOREIGN
GA01946-UK	PIXEL 4A 5G CLEARLY WHITE 128GB CORE UK
GA01946-JP	PIXEL 4A 5G CLEARLY WHITE 128GB JAPAN
GA00677-UK	PIXEL 4XL BLACK 128GB CORE UK
GA01218-US	PIXEL 4XL BLACK 128GB FOREIGN US
GA01180-UK	PIXEL 4XL BLACK 64GB CORE UK
GA01180-DE	PIXEL 4XL JUST BLACK 64GB FOREIGN
GA01199-US	PIXEL 4XL JUST BLACK 64GB FOREIGN
GA01180-US	PIXEL 4XL JUST BLACK 64GB FOREIGN
GA01180-AU	PIXEL 4XL JUST BLACK 64GB FOREIGN AU
GA01369-US	PIXEL 4XL JUST BLACK 64GB FOREIGN US
GA01194-US	PIXEL 4XL JUST BLACK 64GB FOREIGN US
GA01185-UK	PIXEL 4XL ORANGE 128GB CORE UK
GA01182-UK	PIXEL 4XL ORANGE 64GB CORE UK
GA01184-UK	PIXEL 4XL WHITE 128GB CORE UK
GA01181-UK	PIXEL 4XL WHITE 64GB CORE UK
GA01181-DE	PIXEL 4XL CLEARLY WHITE 64GB FOREIGN
GA01205-US	PIXEL 4XL CLEARLY WHITE 64GB FOREIGN
GA01207-US	PIXEL 4XL CLEARLY WHITE 64GB FOREIGN
GA01181-US	PIXEL 4XL CLEARLY WHITE 64GB FOREIGN US
GA01370-US	PIXEL 4XL CLEARLY WHITE 64GB FOREIGN US
GA01316-UK	PIXEL 5 JUST BLACK 128GB CORE UK
GA02633-UK	PIXEL 5 JUST BLACK 128GB DEMO UK
GA01316-AU	PIXEL 5 JUST BLACK 128GB FOREIGN AU
GA01316-CA	PIXEL 5 JUST BLACK 128GB FOREIGN CA
GA01316-DE	PIXEL 5 JUST BLACK 128GB FOREIGN DE
GA01316-JP	PIXEL 5 JUST BLACK 128GB FOREIGN JP
GA01955-US	PIXEL 5 JUST BLACK 128GB FOREIGN US
GA01316-US	PIXEL 5 JUST BLACK 128GB FOREIGN US
GA01967-US	PIXEL 5 JUST BLACK 128GB FOREIGN US
GA01979-US	PIXEL 5 JUST BLACK 128GB FOREIGN US
GA01986-UK	PIXEL 5 SAGE GREEN 128GB CORE UK
GA01986-JP	PIXEL 5 SAGE GREEN 128GB FOREIGN (JP)
GA01980-US	PIXEL 5 SAGE GREEN 128GB FOREIGN (US)
GA02618-JP	PIXEL 5A 5G MOSTLY BLACK 128GB FOREIGN (JP)
GA02618-US	PIXEL 5A 5G MOSTLY BLACK 128GB FOREIGN (US)
GA02900-GB	PIXEL 6 BLACK (CARBON)(STORMY BLACK) 128GB CORE UK
GA03347-GB	PIXEL 6 BLACK (CARBON)(STORMY BLACK) 128GB CORE UK DEMO
GA02900-EU-RA	PIXEL 6 BLACK (CARBON)(STORMY BLACK) 128GB (RA)
GA02900-FR	PIXEL 6 BLACK (CARBON)(STORMY BLACK) 128GB FRANCE
GA02900-JP	PIXEL 6 BLACK (CARBON)(STORMY BLACK) 128GB JP
GA02300-US	PIXEL 6 BLACK (CARBON)(STORMY BLACK) 128GB US
GA04230-US	PIXEL 6 BLACK (CARBON)(STORMY BLACK) 128GB US
GA02900-US	PIXEL 6 BLACK (CARBON)(STORMY BLACK) 128GB US
GA03900-GB	PIXEL 6 BLACK (CARBON)(STORMY BLACK) 256GB CORE UK
GA02910-GB	PIXEL 6 GREY (FOG)(SORTA SEAFOAM) 128GB CORE UK
GA02910-FR	PIXEL 6 GREY (FOG)(SORTA SEAFOAM) 128GB FOREIGN FR
GA02910-US	PIXEL 6 GREY (FOG)(SORTA SEAFOAM) 128GB FOREIGN US
GA03100-US	PIXEL 6 GREY (FOG)(SORTA SEAFOAM) 128GB FOREIGN US
GA02920-GB	PIXEL 6 RED (POMELO)(KINDA CORAL) 128GB CORE UK
GA02910-JP	PIXEL 6 RED (POMELO)(KINDA CORAL) 128GB FOREIGN JP
GA02920-US	PIXEL 6 RED (POMELO)(KINDA CORAL) 128GB FOREIGN US
GA03164-GB	PIXEL 6 PRO STORMY BLACK (CARBON) 128GB CORE UK
GA03165-EU-RA	PIXEL 6 PRO CLOUDY WHITE (PAPER) 128GB CORE UK
GA03166-EU-RA	PIXEL 6 PRO SORTA SUNNY (SUN) 128GB CORE UK
GA03361-GB	PIXEL 6 PRO STORMY BLACK (CARBON) 128GB DEMO
GA03158-FR	PIXEL 6 PRO STORMY BLACK (CARBON) 128GB FOREIGN
GA03140-US	PIXEL 6 PRO STORMY BLACK (CARBON) 128GB FOREIGN
GA03149-US	PIXEL 6 PRO STORMY BLACK (CARBON) 128GB FOREIGN
GA03146-US	PIXEL 6 PRO STORMY BLACK (CARBON) 128GB FOREIGN
GA03137-US	PIXEL 6 PRO STORMY BLACK (CARBON) 128GB FOREIGN
GA03161-CA	PIXEL 6 PRO STORMY BLACK (CARBON) 128GB FOREIGN
GA03167-AU	PIXEL 6 PRO STORMY BLACK (CARBON) 128GB FOREIGN
GA03164-EU-RA	PIXEL 6 PRO STORMY BLACK (CARBON) 128GB
GA02258-GB	PIXEL 6 PRO STORMY BLACK (CARBON) 256GB CORE UK
GA02231-US	PIXEL 6 PRO STORMY BLACK (CARBON) 256GB FOREIGN US
GA03166-GB	PIXEL 6 PRO SORTA SUNNY (SUN) 128GB CORE UK
GA03151-US	PIXEL 6 PRO SORTA SUNNY (SUN) 128GB FOREIGN (US)
GA03165-GB	PIXEL 6 PRO CLOUDY WHITE (PAPER) 128GB CORE UK
GA03168-AU	PIXEL 6 PRO CLOUDY WHITE (PAPER) 128GB FOREIGN AU
GA03138-US	PIXEL 6 PRO CLOUDY WHITE (PAPER) 128GB FOREIGN US
GA03150-US	PIXEL 6 PRO CLOUDY WHITE (PAPER) 128GB FOREIGN US
GA02229-US	PIXEL 6 PRO CLOUDY WHITE (PAPER) 256GB FOREIGN US
GA02998-GB	PIXEL 6A CHARCOAL 128GB CORE UK
GA02998-US	PIXEL 6A CHARCOAL 128GB FOREIGN US
GA03715-GB	PIXEL 6A SAGE GREEN 128GB CORE UK
GA03714-GB	PIXEL 6A CHALK WHITE 128GB CORE UK
GA03923-GB	PIXEL 7 BLACK OBSIDIAN 128GB CORE UK
GA03923-JP	PIXEL 7 BLACK OBSIDIAN 128GB FOREIGN JP
GA03923-US	PIXEL 7 BLACK OBSIDIAN 128GB FOREIGN US
GA04528-GB	PIXEL 7 BLACK OBSIDIAN 256GB CORE UK
GA03933-GB	PIXEL 7 SNOW 128GB CORE UK
GA04538-GB	PIXEL 7 SNOW 256GB CORE UK
GA03943-GB	PIXEL 7 LEMONGRASS 128GB CORE UK
GA03943-US	PIXEL 7 LEMONGRASS 128GB FOREIGN US
GA04548-GB	PIXEL 7 LEMONGRASS 256GB CORE UK
GA03462-GB	PIXEL 7 PRO OBSIDIAN 128GB CORE UK
GA03462-EU-RA	PIXEL 7 PRO OBSIDIAN 128GB CORE UK
GA03423-US	PIXEL 7 PRO OBSIDIAN 128GB FOREIGN US
GA03453-US	PIXEL 7 PRO OBSIDIAN 128GB FOREIGN US
GA03463-EU-RA	PIXEL 7 PRO SNOW 128GB CORE UK
GA03465-GB	PIXEL 7 PRO OBSIDIAN 256GB CORE UK
GA03426-US	PIXEL 7 PRO OBSIDIAN 256GB FOREIGN US
GA03417-US	PIXEL 7 PRO OBSIDIAN 256GB FOREIGN US
GA03464-GB	PIXEL 7 PRO HAZEL GREEN 128GB CORE UK
GA03425-US	PIXEL 7 PRO HAZEL GREEN 128GB FOREIGN US
GA03416-US	PIXEL 7 PRO HAZEL GREEN 128GB FOREIGN US
GA03455-US	PIXEL 7 PRO HAZEL GREEN 128GB FOREIGN US
GA03467-GB	PIXEL 7 PRO HAZEL GREEN 256GB CORE UK
GA03458-US	PIXEL 7 PRO HAZEL GREEN 256GB FOREIGN US
GA03419-US	PIXEL 7 PRO HAZEL GREEN 256GB FOREIGN US
GA03463-GB	PIXEL 7 PRO SNOW 128GB CORE UK
GA03466-GB	PIXEL 7 PRO SNOW 256GB CORE UK
GA03457-US	PIXEL 7 PRO SNOW 256GB FOREIGN US
GA03933-EU-RA	PIXEL 7 SNOW 128GB CORE UK
GA03694-GB	PIXEL 7A CARBON BLACK (CHARCOAL) 128GB CORE UK
GA04275-GB	PIXEL 7A ARCTIC BLUE (SEA) 128GB CORE UK
GA04438-GB	PIXEL 7A REAL RED (CORAL) 128GB CORE UK
GA04274-GB	PIXEL 7A COTTON WHITE (SNOW) 128GB CORE UK
GA04823-GB	PIXEL 8 HAZEL 128GB CORE UK
GA04861-GB	PIXEL 8 HAZEL 256GB CORE UK
GA04859-GB	PIXEL 8  MINT 128GB CORE UK
GA04803-GB	PIXEL 8 OBSIDIAN (LICORICE) 128GB CORE UK
GA04833-GB	PIXEL 8 OBSIDIAN (LICORICE) 256GB CORE UK
GA04856-GB	PIXEL 8 ROSE (PEONY) 128GB CORE UK
GA05000-GB	PIXEL 8 ROSE (PEONY) 256GB CORE UK
GA04841-GB	PIXEL 8 PRO BAY (SKY) 128GB CORE UK
GA04915-GB	PIXEL 8 PRO BAY (SKY) 256GB CORE UK
GA05175-GB	PIXEL 8 PRO MINT 128GB CORE UK
GA04798-GB	PIXEL 8 PRO OBSIDIAN 128GB CORE UK
GA04890-GB	PIXEL 8 PRO OBSIDIAN 256GB CORE UK
GA04921-GB	PIXEL 8 PRO OBSIDIAN 512GB CORE UK
GA04834-GB	PIXEL 8 PRO PORCELAIN 128GB CORE UK
GA04905-GB	PIXEL 8 PRO PORCELAIN 256GB CORE UK
GA04411-US	PIXEL FOLD OBSIDIAN 256GB CORE
GA04413-US	PIXEL FOLD OBSIDIAN 512GB CORE
GA04412-US	PIXEL FOLD PORCELAIN 256GB CORE
GA04304-GB	PIXEL WATCH LTE MATTE BLACK STAINLESS STEEL CASE/OBSIDIAN ACTIVE BAND
GA04121-GB	PIXEL WATCH LTE GOLD STAINLESS CASE/HAZEL ACTIVE BAND
GA04305-GB	PIXEL WATCH LTE POLISHED SILVER STAINLESS STEEL CASE/CHALK ACTIVE BAND
GA04307-GB	PIXEL WATCH LTE POLISHED SILVER CASE/CHARCOAL ACTIVE BAND
GA04432-GB	PIXEL 8A BLACK (OBSIDIAN) 128GB CORE UK
GA05571-GB	PIXEL 8A BLACK (OBSIDIAN) 256GB CORE UK
GA05570-GB	PIXEL 8A BLUE (BAY) 128GB CORE UK
GA05595-GB	PIXEL 8A GREEN (ALOE) 128GB CORE UK
GA04988-GB	PIXEL 8A WHITE (PORCELAIN) 128GB CORE UK

"""

product_dict = utils.create_product_dict(product_data)

def get_product_description(sku_value):
    # Check if SKU exists in the dictionary
    if sku_value in product_dict:
        # Return the description associated with the SKU
        return product_dict[sku_value]
    else:
        # Return a message if SKU is not found
        return f"SKU {sku_value} not found."

# get_product_description('GA02910-GB')
# result = get_product_description('GA02910-GB')
# print(result)


