import pytesseract
from PIL import Image, ImageFilter
import re


def extract_text(image_path):

    image = Image.open(image_path)

    # Increaase image resolution x4
    scale_factor = 4
    new_width = int(image.width * scale_factor)
    new_height = int(image.height * scale_factor)
    high_res_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Improve edges 
    high_res_image = high_res_image.filter(ImageFilter.SHARPEN)

    # Remove noise
    high_res_image = high_res_image.filter(ImageFilter.MedianFilter(size=3))

    # increasing text contrast
    # threshold = 128
    # high_res_image = high_res_image.point(lambda x: 255 if x > threshold else 0)

    # Convert to gray scale
    high_res_image = high_res_image.convert("L")

    # Save the preprocessed image for debugging
    high_res_image.save("12.png")

    custom_config = r'--psm 6'

    extracted_text = pytesseract.image_to_string(high_res_image, config=custom_config)

    print(extracted_text)
    return extracted_text

# Get the type of the report

def process_report_data(extracted_text):
    # {type:keywords} 
    types = {'blood sugar' : ['blood sugar'], 'full blood count' : ['full blood count', 'complete blood count']}
    type = ''

    for key, value in types.items():
        pattern = '|'.join(value)

        match = re.search(pattern, extracted_text, re.IGNORECASE)
        if match:
            if match.group().lower() in value:
                type = key
                break

    if type == '':
        print("Type does not found. Or type does not support.")

    print('Type is: ' + type)

    # Get the values based on the types
    data = {}
    if type == 'full blood count':
        data['platelet count'] = (['platelet count'], 0)
        data['white cell count'] = (['white cell count'], 0)


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
    data_final['gender'] = 'male'
    data_final['age'] = 24
    data_final['data'] = {}

    for key,value in data.items():
        data_final['data'][key] = {'value': value[1]}

    print(data_final)
    return data_final





def add_reference_data(data_final):
    # Add normal values to the data structre
    normal_data = {
        'full blood count': {
            'platelet count': {
                'world average': 300,
                'sri lankan average': 305,
                'male average': 310,
                'female average': 302,
                '20 lower average': 290,
                '40 lower average': 295,
                '60 lower average': 280,
                '80 lower average': 298
            },
            'white cell count': {
                'world average': 300,
                'sri lankan average': 305,
                'male average': 310,
                'female average': 302,
                '20 lower average': 290,
                '40 lower average': 295,
                '60 lower average': 280,
                '80 lower average': 298
            }
        },
        'blood sugar': {
            'fasting': {
                'world average': 90,
                'sri lankan average': 92,
                'male average': 94,
                'female average': 91,
                '20 lower average': 85,
                '40 lower average': 88,
                '60 lower average': 87,
                '80 lower average': 89
            },
            'postprandial': {
                'world average': 120,
                'sri lankan average': 122,
                'male average': 124,
                'female average': 121,
                '20 lower average': 115,
                '40 lower average': 118,
                '60 lower average': 117,
                '80 lower average': 119
            }
        }
    }

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

    print(data_final)
    return data_final