import scrapy
import re
from itemloaders.processors import MapCompose, TakeFirst

# Extracts media if text matches words in media_words
def extract_media(raw_str):
    media_words = ['board', 'vinyl', 'acrylic', 'wood', 'veneers', 'card', 'spraypaint', 'sculpture', 'charcoal', 'resin', 'pigment', 'leaf', 'concrete',
                   'canvas', 'crystal', 'iron', 'inkjet', 'laser', 'paper', 'pencil', 'cement', 'gold', 'watercolour', 'pigments', 'pins', 'ground', 'media',
                   'aluminium', 'oil', 'ink', 'digital', 'copper', 'procelain', 'wire', 'mixed', 'print', 'mdf', 'beech', 'laser', 'steel', 'enamel']

    raw_str_lower = raw_str.lower()
    splitted_raw_str = re.split(',', raw_str_lower)
    matching_strs = [string for string in splitted_raw_str
                     if any(word in string for word in media_words) and len(string.split()) < 15]
    if matching_strs:
        out_str = ', '.join(matching_strs).strip()
        return out_str

# Extracts height if text matches regex pattern
def extract_height(raw_str):
    splitted_raw_str = re.split(',', raw_str)
    for element in splitted_raw_str:
        if bool(re.search(r'\d+\s*(?:[cC][mM])?\s*[xX]\s*\d+\s*(?:[cC][mM])?', element)):
            dim_list = re.split('[xX]', element)
            return float(re.sub(r'[^\d.]+', '', dim_list[0]))
        elif bool(re.search(r'\d+\s*(?:[cC][mM])\s*(?:diam\s*)?', element)):
            dim_list = re.split(' ', element)
            return float('NaN')
            # return float(re.sub(r'[^\d.]+', '', dim_list[0]))

# Extracts width if text matches regex pattern
def extract_width(raw_str):
    splitted_raw_str = re.split(',', raw_str)
    for element in splitted_raw_str:
        if bool(re.search(r'\d+\s*(?:[cC][mM])?\s*[xX]\s*\d+\s*(?:[cC][mM])?', element)):
            dim_list = re.split('[xX]', element)
            return float(re.sub(r'[^\d.]+', '', dim_list[1]))
        elif bool(re.search(r'\d+\s*(?:[cC][mM])\s*(?:diam\s*)?', element)):
            dim_list = re.split(' ', element)
            return float('NaN')
            # return float(re.sub(r'[^\d.]+', '', dim_list[1]))

# Extracts price if text matches regex pattern
def extract_price(price_str):
    return float(re.sub(r'[^\d.]', '', price_str))


class ProductItem(scrapy.Item):
    # define the fields for your item here like:
    product_url = scrapy.Field(
        output_processor=TakeFirst())

    title = scrapy.Field(
        output_processor=TakeFirst())

    media = scrapy.Field(
        input_processor=MapCompose(extract_media),
        output_processor=TakeFirst())

    height_cm = scrapy.Field(
        input_processor=MapCompose(extract_height),
        output_processor=TakeFirst())

    width_cm = scrapy.Field(
        input_processor=MapCompose(extract_width),
        output_processor=TakeFirst())

    price_gbp = scrapy.Field(
        input_processor=MapCompose(extract_price),
        output_processor=TakeFirst())

    fields_to_export = ['title', 'product_url',
                        'media', 'height_cm', 'width_cm', 'price']
