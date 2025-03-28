import pytesseract
from PIL import Image, ImageFilter
import re
import data.normal_data as db_normal_data
import data.types as db_types
from data.type_fields import type_field_getter

class TypeNotSupportError(Exception):
    pass

def extract_text(image_path):

    image = Image.open(image_path)

    image = image.convert("RGB")

    # Increaase image resolution x4
    # scale_factor = 4
    # new_width = int(image.width * scale_factor)
    # new_height = int(image.height * scale_factor)
    # high_res_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Improve edges 
    # high_res_image = high_res_image.filter(ImageFilter.SHARPEN)

    # Remove noise
    # high_res_image = high_res_image.filter(ImageFilter.MedianFilter(size=3))

    # increasing text contrast
    # threshold = 128
    # high_res_image = high_res_image.point(lambda x: 255 if x > threshold else 0)

    # Convert to gray scale
    high_res_image = image.convert("L")

    # Save the preprocessed image for debugging
    # high_res_image.save("12.png")

    custom_config = r'--psm 6'

    extracted_text = pytesseract.image_to_string(high_res_image, config=custom_config)

    print(extracted_text)
    return extracted_text

# Get the type of the report

def process_report_data(extracted_text, age, gender):
    # {type:keywords} 
    types = db_types.types
    type = ''

    for key, value in types.items():
        pattern = '|'.join(value)

        match = re.search(pattern, extracted_text, re.IGNORECASE)
        if match:
            if match.group().lower() in value:
                type = key
                break

    if type == '':
        raise TypeNotSupportError("Type does not found. Or type does not support.")

    # print('Type is: ' + type)

    # Get the values based on the types
    data = type_field_getter(type)


    for key, value in data.items():
        pattern = '|'.join(value[0])

        match = re.search(pattern, extracted_text, re.IGNORECASE)
        if match:
            start = match.end()+1
            end = start
            while end < len(extracted_text) and not extracted_text[end].isspace():
                end += 1
            extracted_value = extracted_text[start:end].strip()
            data[key] = (value[0], extracted_value)


    print(data)

    # make the final data structre 
    data_final = {}
    data_final['type'] = type
    data_final['gender'] = gender
    data_final['age'] = age
    data_final['data'] = {}

    for key,value in data.items():
        data_final['data'][key] = {'value': value[1]}

    print(data_final)
    return data_final


def add_reference_data(data_final):
    # Add normal values to the data structre
    normal_data = db_normal_data.normal_data

    if data_final['type'] in normal_data:
        for key in data_final['data']:
            data_final['data'][key]['world average'] = normal_data[data_final['type']][key]['world average']
            data_final['data'][key]['sri lankan average'] = normal_data[data_final['type']][key]['sri lankan average']
            
            if data_final['gender'] == 'male':
                data_final['data'][key]['male average'] = normal_data[data_final['type']][key]['male average']
            elif data_final['gender'] == 'female':
                data_final['data'][key]['female average'] = normal_data[data_final['type']][key]['female average']
            
            if data_final['age'] < 20:
                data_final['data'][key]['20 lower average'] = normal_data[data_final['type']][key]['20 lower average']
            elif data_final['age'] < 40:
                data_final['data'][key]['40 lower average'] = normal_data[data_final['type']][key]['40 lower average']
            elif data_final['age'] < 40:
                data_final['data'][key]['60 lower average'] = normal_data[data_final['type']][key]['60 lower average']
            elif data_final['age'] < 40:
                data_final['data'][key]['80 lower average'] = normal_data[data_final['type']][key]['80 lower average']

    # print(data_final)
    return data_final