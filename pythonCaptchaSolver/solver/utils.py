import time
import random
import base64
import cv2
import numpy as np

def human_delay(min_ms=100, max_ms=500):
    time.sleep(random.uniform(min_ms, max_ms) / 1000)

def decode_base64_image(data_url):
    header, encoded = data_url.split(",", 1)
    binary = base64.b64decode(encoded)
    nparr = np.frombuffer(binary, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img
