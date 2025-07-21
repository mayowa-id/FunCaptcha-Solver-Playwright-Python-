import cv2
import os
from .core import launch_browser, find_fcaptcha_frame, capture_canvas, detect_rotation_angle, simulate_rotation
from .utils import human_delay

def extract_canvas():
    print("[TEST MODE] Extracting canvas image...")
    page, browser, p = launch_browser()
    try:
        frame = find_fcaptcha_frame(page)
        img = capture_canvas(frame)
        save_path = "output/extracted_canvas.png"
        os.makedirs("output", exist_ok=True)
        cv2.imwrite(save_path, img)
        print(f"[✓] Canvas image saved to {save_path}")
        input("Press Enter to close browser...")
    finally:
        browser.close()
        p.stop()

def test_rotation_angle():
    print("[TEST MODE] Estimating rotation angle from saved canvas image...")
    img = cv2.imread("output/extracted_canvas.png")
    if img is None:
        print("[x] No canvas image found. Run --mode=extract first.")
        return
    angle = detect_rotation_angle(img)
    print(f"[✓] Estimated rotation angle: {angle:.2f}°")

def simulate_drag_only():
    print("[TEST MODE] Simulating drag without solving...")
    page, browser, p = launch_browser()
    try:
        frame = find_fcaptcha_frame(page)
        simulate_rotation(frame, drag_pixels=40)
        print("[✓] Drag simulation completed.")
        input("Press Enter to close browser...")
    finally:
        browser.close()
        p.stop()

def full_test_flow():
    print("[TEST MODE] Full flow dry-run (no CAPTCHA submission)...")
    page, browser, p = launch_browser()
    try:
        frame = find_fcaptcha_frame(page)
        image = capture_canvas(frame)
        angle = detect_rotation_angle(image)
        pixels = int((angle / 30) * 100)
        print(f"Detected angle: {angle:.2f}°, dragging {pixels} pixels")
        simulate_rotation(frame, drag_pixels=pixels)
        input("Press Enter to close browser...")
    finally:
        browser.close()
        p.stop()
