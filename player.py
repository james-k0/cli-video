import os
import time
from PIL import Image
import numpy as np

ASCII_CHARS = ['@', '#', '8', '&', '%', '$', '!', ':', '*', '+', '=', '-', '.', ' ']

# grayscale and fit
def image_to_ascii(image_path, new_width=100):
    img = Image.open(image_path)
    
    # 8 bit per channel and greyscale 
    img = img.convert('L')
    
    # magic code to keep font same size
    width, height = img.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)  # 0.55 is that magic number
    img = img.resize((new_width, new_height))

    img_array = np.array(img) #there has to be a better way to do this surely

    
    ascii_str = ''
    for row in img_array:
        for pixel in row:
            ascii_str += ASCII_CHARS[pixel // 25]  # div 25 maps to the charset
        ascii_str += '\n'

    return ascii_str


def display_images_from_folder(folder_path, new_width=100, fps=10):
    # grab all images
    images = [f for f in os.listdir(folder_path) if f.endswith('.png')]
    
    if not images:
        print("No PNG images found in the folder.")
        return
    
    while True:  #main
        for filename in images:
            image_path = os.path.join(folder_path, filename)
            #print(f"\nDisplaying {filename} as ascii\n")
            os.system(f"title playing {filename}")
            ascii_art = image_to_ascii(image_path, new_width)
            print(ascii_art)

            #python sleep is notoriously incorrect, i dont know any alternatives
            time.sleep(1 / fps)


folder_path = 'apple'
fps = 30
display_images_from_folder(folder_path, fps)
