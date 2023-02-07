import sys
sys.path.append("../")
import os
from kivy.app import App
from handle_image import convert_to_binary, resize_image
from kivy.uix.widget import Widget
from client import Client
from kivy.clock import Clock
from kivy.uix.camera import Camera
import cv2 as cv
from kivy.graphics.texture import Texture
from PIL import Image
import numpy as np
import pickle
from threading import Thread
from functools import partial
from time import time


class MainWidget(Widget):
    def __init__(self, **kwargs):
        Widget.__init__(self, **kwargs)
        self.client = None
        Clock.schedule_interval(self.send, 0.5)
        self.send_msg = None
        self.binary_img = None
        self.capture = cv.VideoCapture("https://192.168.1.5:8080/video")

    def send_thread(self):
        first = time()
        #msg = self.client.send(self.send_msg, data_type="image")
        msg = self.client.send(self.binary_img, data_type="binary_img")
        print(f"send in {time() - first}")

    def send(self, dt):
        try:
            if self.client:
                ret, frame = self.capture.read()
                frame = resize_image(frame)
                self.send_msg = frame.tolist()
                binary_img = convert_to_binary(frame)
                self.binary_img = binary_img.tolist()
                thread = Thread(target=self.send_thread)
                thread.start()
        except Exception as e:
            print(e)
            print("Waiting for camera ...")

    def _get_client(self, third, final):
        ip = "192.168." + third + "." + final
        port = 1234
        self.client = Client(ip, port, "Cam")

    def connect(self):
        third = self.ids.third.text
        final = self.ids.final.text
        msg = self._get_client(third, final)


class TheCameraApp(App):
    pass 


if __name__ == "__main__":
    TheCameraApp().run()
