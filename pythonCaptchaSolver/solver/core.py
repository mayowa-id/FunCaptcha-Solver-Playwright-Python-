import cv2
import numpy as np
import base64
import os
from .utils import decode_base64_image, human_delay

def launch_browser():
    from playwright.sync_api import sync_playwright
    from dotenv import load_dotenv

    load_dotenv()
    TARGET_URL = os.getenv("TARGET_URL")

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
    print("[*] Capturing canvas from iframe...")
    base64_data = frame.evaluate("""
        () => {
            const canvas = document.querySelector('canvas');
            return canvas.toDataURL();
        }
    """)
    img = decode_base64_image(base64_data)
    return img

def detect_rotation_angle(image):
    # Replace this with your real ML or template matching logic later
    print("[*] Estimating rotation angle (placeholder logic)...")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest = max(contours, key=cv2.contourArea)
        angle = cv2.minAreaRect(largest)[-1]
        if angle < -45:
            angle = 90 + angle
        return -angle
    else:
        return 0.0

def simulate_rotation(frame, drag_pixels=50):
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
    human_delay(400, 600)
    frame.mouse.move(start_x + drag_pixels, start_y, steps=15)
    human_delay(300, 500)
    frame.mouse.up()

    print(f"[✓] Dragged {drag_pixels}px simulating rotation.")

def wait_for_success(frame):
    print("[*] Waiting to detect CAPTCHA completion...")
    try:
        frame.wait_for_selector("text=You passed", timeout=10000)
        print("[✓] CAPTCHA successfully solved!")
        return True
    except:
        print("[x] CAPTCHA may not have been solved.")
        return False

def solve_fcaptcha():
    page, browser, p = launch_browser()
    try:
        frame = find_fcaptcha_frame(page)
        image = capture_canvas(frame)
        angle = detect_rotation_angle(image)
        print(f"[✓] Detected rotation angle: {angle:.2f}°")

        # Assume max 30° = 100px drag range (empirical)
        drag_pixels = int((angle / 30.0) * 100)
        print(f"[*] Calculated drag pixels: {drag_pixels}")

        simulate_rotation(frame, drag_pixels)
        human_delay(1500, 2000)
        wait_for_success(frame)

        input("Press Enter to close browser...")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        browser.close()
        p.stop()
