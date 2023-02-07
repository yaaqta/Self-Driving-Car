import cv2 as cv 
import numpy as np
from PIL import Image
import socket


def load_img(file):
    with open(file, 'r') as file:
        data = file.read()
        data = data.split('\n')
        data.pop()


    for i in range(len(data)):
        data[i] = data[i].split(',')

    return data


def convert_into_matrix(data):
    for i in range(len(data)):
        for j in range(len(data[0])):
            data[i][j] = int(data[i][j])

    return data


def convert_csv_to_image(file):
    data = load_img(file)
    data = convert_into_matrix(data)
    copy_data = data.copy()
    img = np.array(data)
    image = Image.fromarray(img.astype(np.uint8), "L")
    image.save("labview\\image.png")
    print("Image is saved.")
    return copy_data

if __name__ == "__main__":
    pass 
