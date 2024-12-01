import pandas as pd
from PIL import Image
import os

# Load Excel
df = pd.read_excel('movies_dataset.xlsx')

# Correct the image path
image_path = df['Image_Path'][0]
image_path = os.path.normpath(image_path)  # Normalizes path if any slashes are off

# Load and display the image
img = Image.open(image_path)
img.show()
