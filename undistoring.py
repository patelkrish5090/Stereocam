import cv2
import numpy as np

# Load the camera calibration parameters
# Replace these with your actual calibration parameters
camera_matrix = np.array([[1000.0, 0.0, 320.0],
                          [0.0, 1000.0, 240.0],
                          [0.0, 0.0, 1.0]], dtype=np.float32)
dist_coeffs = np.array([0.1, -0.25, 0.001, 0.001, 0.0], dtype=np.float32)

# Load the image to undistort
image = cv2.imread('distorted_image.jpg')

# Undistort the image
undistorted_image = cv2.undistort(image, camera_matrix, dist_coeffs)

# Save or display the undistorted image
cv2.imwrite('undistorted_image.jpg', undistorted_image)

# Optionally display the images using OpenCV's imshow function
cv2.imshow('Original Image', image)
cv2.imshow('Undistorted Image', undistorted_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
