import pytesseract
from PIL import Image, ImageFilter
import re

image_path = "1.webp"

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

# Get the type of the report

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
