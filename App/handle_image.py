import cv2 as cv 
import numpy as np


def resize_image(image):
    image = cv.resize(image, (200, 125))
    return image


def convert_to_gray(image):
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    return gray_image


def convert_to_binary(image):
    image = resize_image(image)
    gray_image = convert_to_gray(image)
    (thresh, b_image) = cv.threshold(gray_image, 128, 255, cv.THRESH_BINARY)
    return b_image


if __name__ == "__main__":
    image = cv.imread("../images/enter_ip.png")
    image = resize_image(image)
    gray_image = convert_to_binary(image)
    print(gray_image.tolist())
    cv.imshow("gray_image", gray_image)
    cv.waitKey()
    cv.destroyAllWindows()
