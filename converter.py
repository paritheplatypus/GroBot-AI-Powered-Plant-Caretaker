import base64

# Use a raw string for the image path
image_path = r'C:\Users\phppa\OneDrive\Desktop\Tomato-plant-fusarium-disease(3).jpg'

with open(image_path, 'rb') as image_file:
    base64_string = base64.b64encode(image_file.read()).decode('utf-8')

print(base64_string)
