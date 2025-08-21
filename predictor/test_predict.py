import sys
from predict import tensorflow_pred

# Example image URL (must be replaced with a real traffic image URL)
image_url = 'https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png'

if len(sys.argv) > 1:
    image_url = sys.argv[1]

result = tensorflow_pred(image_url)
print(f'Prediction result: {result}')
