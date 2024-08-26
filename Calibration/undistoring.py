import cv2
import numpy as np

# Load the camera calibration parameters
# Replace these with your actual calibration parameters
camera_matrix = np.array([[4.82554559e+03, 0.00000000e+00, 3.61280513e+02],
                          [0.00000000e+00, 4.68278228e+03, 1.12506458e+02],
                          [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]], dtype=np.float32)
dist_coeffs = np.array([[ 4.49166719e-01,  2.87671697e+00, -1.03479154e-02, -1.35482683e-01, -1.85246457e+01]], dtype=np.float32)

# Load the image to undistort
image = cv2.imread('images/img3.png')

# Undistort the image
undistorted_image = cv2.undistort(image, camera_matrix, dist_coeffs)

# Save or display the undistorted image
cv2.imwrite('undistorted_image.jpg', undistorted_image)

# Optionally display the images using OpenCV's imshow function
cv2.imshow('Original Image', image)
cv2.imshow('Undistorted Image', undistorted_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
