# catptchaSollver.py

from playwright.sync_api import sync_playwright, TimeoutError
import time
import random
import os
from dotenv import load_dotenv
import base64
import numpy as np
import cv2
cv2.__version__

import os
from datetime import datetime

import os

# Create a folder next to your script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(SCRIPT_DIR, "funcaptcha_frames")
os.makedirs(output_dir, exist_ok=True)
output_dir, os.listdir(output_dir)


load_dotenv()
TARGET_URL = os.getenv("TARGET_URL")


def human_delay(min_ms=100, max_ms=500):
    time.sleep(random.uniform(min_ms, max_ms) / 1000)


def launch_browser():
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    print("[*] Navigating to FunCaptcha page...")
    page.goto(TARGET_URL)
    return page, browser, p


def find_fcaptcha_frame(page):
    print("[*] Searching for FunCaptcha iframe...")
    for frame in page.frames:
        if "funcaptcha" in frame.url:
            print(f"[✓] FunCaptcha frame found: {frame.url}")
            return frame
    raise Exception("FunCaptcha iframe not found")


def capture_canvas(frame):
    try:
        canvas = frame.wait_for_selector("canvas", timeout=10000)
        print("[✓] Canvas detected!")

        # Get base64 screenshot from canvas
        base64_data = frame.evaluate("""
            () => {
                const canvas = document.querySelector('canvas');
                return canvas.toDataURL().split(',')[1];  // Remove "data:image/png;base64,"
            }
        """)

        image_data = base64.b64decode(base64_data)
        np_arr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        print("[✓] Canvas image decoded to OpenCV format.")
        return img

    except TimeoutError:
        print("[x] Canvas element not found inside iframe.")
        return None


def simulate_rotation(frame, drag_pixels=50):
    print(f"[*] Simulating drag of {drag_pixels}px...")
    try:
        canvas = frame.query_selector("canvas")
        if not canvas:
            raise Exception("Canvas not found for interaction.")

        box = canvas.bounding_box()
        if not box:
            raise Exception("Could not determine canvas bounds.")

        start_x = box["x"] + box["width"] / 2
        start_y = box["y"] + box["height"] / 2

        frame.mouse.move(start_x, start_y)
        human_delay(200, 400)
        frame.mouse.down()
        human_delay(300, 500)

        frame.mouse.move(start_x + drag_pixels, start_y, steps=10)
        human_delay(200, 400)
        frame.mouse.up()

        print("[✓] Canvas drag/rotation complete.")
    except Exception as e:
        print(f"[x] Mouse simulation failed: {e}")


def solve_fcaptcha():
    page, browser, p = launch_browser()
    try:
        human_delay(1000, 1500)
        frame = find_fcaptcha_frame(page)

        # Get image
        image = capture_canvas(frame)
        if image is None:
            raise Exception("Canvas image capture failed")

        # Analyze rotation
        angle = detect_rotation_angle(image)
        pixels = angle_to_drag_pixels(angle)

        # Interact with the canvas using the detected drag
        simulate_rotation(frame, drag_pixels=pixels)

        input("Press Enter to close browser...")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        browser.close()
        p.stop()


def capture_multiple_frames(frame, count=10, delay_ms=500):
    """
    Capture `count` screenshots of the FunCaptcha canvas,
    saved as funcaptcha_frames/frame_1.png … frame_count.png
    """
    for i in range(1, count + 1):
        try:
            canvas = frame.wait_for_selector("canvas", timeout=5000)
            path = os.path.join(output_dir, f"frame_{i}.png")
            canvas.screenshot(path=path)
            print(f"[✓] Captured frame {i} → {path}")
            human_delay(delay_ms, delay_ms + 200)
        except TimeoutError:
            print(f"[!] Frame {i}: canvas not found.")

def detect_rotation_angle(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        print("[!] No contours found.")
        return 0

    # Find largest contour
    largest = max(contours, key=cv2.contourArea)
    rect = cv2.minAreaRect(largest)
    angle = rect[-1]

    # OpenCV returns angle between [-90, 0); adjust it
    if angle < -45:
        angle = 90 + angle

    print(f"[✓] Detected rotation angle: {angle:.2f} degrees")
    return angle

def angle_to_drag_pixels(angle, max_angle=30, max_pixels=100):
    angle = max(-max_angle, min(max_angle, angle))  # Clamp angle
    drag_pixels = int((angle / max_angle) * max_pixels)
    print(f"[*] Mapped angle {angle:.2f}° to {drag_pixels}px drag.")
    return drag_pixels

def is_captcha_present(page):
    # Check if iframe is still visible
    return any("funcaptcha" in frame.url for frame in page.frames)

def solve_once(page):
    try:
        frame = find_fcaptcha_frame(page)
        capture_canvas(frame)
        simulate_rotation(frame)
        human_delay(1000, 2000)
        return True
    except Exception as e:
        print(f"[!] Error in single solve attempt: {e}")
        return False


if __name__ == "__main__":
    solve_fcaptcha()
