import cv2
import numpy as np


def check_image_quality(image_path):

    image = cv2.imread(image_path)

    if image is None:
        return {
            "quality": "Invalid",
            "score": 0,
            "message": "Unable to read the image."
        }

    height, width = image.shape[:2]

    if width < 200 or height < 200:
        return {
            "quality": "Poor",
            "score": 25,
            "message": "Image resolution is too low. Use a clearer image."
        }

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Blur detection
    sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()

    # Brightness detection
    brightness = np.mean(gray)

    score = 100

    if sharpness < 50:
        score -= 35

    if brightness < 40:
        score -= 30

    if brightness > 230:
        score -= 25

    score = max(0, min(100, score))

    if score >= 75:
        quality = "Good"
        message = "Image quality is suitable for analysis."

    elif score >= 50:
        quality = "Acceptable"
        message = "Image can be analyzed, but a clearer image may improve results."

    else:
        quality = "Poor"
        message = "Image quality may affect prediction accuracy."

    return {
        "quality": quality,
        "score": round(score, 2),
        "message": message,
        "width": width,
        "height": height,
        "sharpness": round(float(sharpness), 2),
        "brightness": round(float(brightness), 2)
    }