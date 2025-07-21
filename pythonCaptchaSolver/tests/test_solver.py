from solver.core import detect_rotation_angle
import cv2

def test_rotation_detection():
    image = cv2.imread("test_samples/sample.png")  # Replace with actual test image
    angle = detect_rotation_angle(image)
    print(f"Detected angle: {angle}")

if __name__ == "__main__":
    test_rotation_detection()
