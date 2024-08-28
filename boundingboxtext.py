# import cv2
# import numpy as np

# def show_rectangle(img, x, y, w, h, window_name):
#     img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
#     cv2.imshow(window_name, img)

# class Stereocam:
#     def __init__(self):
#         self.centers = []

#     def getContours(self, img):
#         self.centers = []
#         imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
#         imgCanny = cv2.Canny(imgBlur, 50, 50)
#         contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

#         bounding_boxes = []
#         for cnt in contours:
#             area = cv2.contourArea(cnt)
#             if area > 100:  # Filter out small contours (you can adjust this threshold)
#                 peri = cv2.arcLength(cnt, True)
#                 approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
#                 x, y, w, h = cv2.boundingRect(approx)
#                 center_x = x + (w / 2)
#                 center_y = y + (h / 2)
#                 self.centers.append((center_x, center_y))
#                 bounding_boxes.append((x, y, w, h))

#         return bounding_boxes

# # Capture from two cameras
# img1 = cv2.VideoCapture(2)
# img2 = cv2.VideoCapture(4)

# camera1 = Stereocam()
# camera2 = Stereocam()

# fl = 0.03  # Focal length (adjust based on your camera)
# camdis = 3  # Distance between the two cameras (adjust based on your setup)

# while True:
#     # Read frames from both cameras
#     ref1, frame1 = img1.read()
#     ref2, frame2 = img2.read()

#     if not ref1 or not ref2:
#         print("Failed to capture from one or both cameras")
#         break

#     # Get contours and bounding boxes from both cameras
#     bounding_boxes1 = camera1.getContours(frame1)
#     bounding_boxes2 = camera2.getContours(frame2)

#     for i, (box1, center1) in enumerate(zip(bounding_boxes1, camera1.centers)):
#         x1, y1, w1, h1 = box1
#         show_rectangle(frame1, x1, y1, w1, h1, 'Camera 1')

#         if i < len(camera2.centers):
#             center2 = camera2.centers[i]
#             disparity = abs(center1[0] - center2[0])
#             distance = (fl * camdis) / disparity if disparity != 0 else float('inf')
#             print(f"Object {i+1} Distance: {distance}")

#     # Show rectangles in both camera windows
#     for box2 in bounding_boxes2:
#         x2, y2, w2, h2 = box2
#         show_rectangle(frame2, x2, y2, w2, h2, 'Camera 2')

#     # Display the 

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release camera resources and close windows
# img1.release()
# img2.release()
# cv2.destroyAllWindows()

# import cv2
# import numpy as np

# # Initialize the cameras (using camera 2 and 4)
# cam_left = cv2.VideoCapture(2)
# cam_right = cv2.VideoCapture(0)

# # Constants
# focal_length_left = 0.03  # in meters
# focal_length_right = 0.06  # in meters
# baseline = 0.01  # Distance between the two cameras in meters (adjust according to your setup)

# def calculate_distance(disparity, focal_length, baseline):
#     # Distance formula
#     if disparity > 0:
#         distance = (focal_length * baseline) / disparity
#     else:
#         distance = np.inf  # Handle case where disparity is zero
#     return distance

# while True:
#     # Capture frames from both cameras
#     ret_left, frame_left = cam_left.read()
#     ret_right, frame_right = cam_right.read()

#     if not ret_left or not ret_right:
#         print("Failed to grab frames")
#         break

#     # Convert frames to HSV for color-based detection (e.g., detecting a red object)
#     hsv_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2HSV)
#     hsv_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2HSV)

#     # Define range for red color and create mask
#     lower_red = np.array([0, 120, 70])
#     upper_red = np.array([10, 255, 255])
#     mask_left = cv2.inRange(hsv_left, lower_red, upper_red)
#     mask_right = cv2.inRange(hsv_right, lower_red, upper_red)

#     # Find contours
#     contours_left, _ = cv2.findContours(mask_left, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     contours_right, _ = cv2.findContours(mask_right, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     if contours_left and contours_right:
#         # Assume the largest contour is the object
#         largest_contour_left = max(contours_left, key=cv2.contourArea)
#         largest_contour_right = max(contours_right, key=cv2.contourArea)

#         # Get bounding box for the object
#         x_left, y_left, w_left, h_left = cv2.boundingRect(largest_contour_left)
#         x_right, y_right, w_right, h_right = cv2.boundingRect(largest_contour_right)

#         # Draw bounding box
#         cv2.rectangle(frame_left, (x_left, y_left), (x_left+w_left, y_left+h_left), (0, 255, 0), 2)
#         cv2.rectangle(frame_right, (x_right, y_right), (x_right+w_right, y_right+h_right), (0, 255, 0), 2)

#         # Calculate the disparity (x-coordinate difference)
#         disparity = abs(x_left - x_right)

#         if disparity > 0:
#             # Calculate distance using the focal length of the left camera
#             distance_left = calculate_distance(disparity, focal_length_left, baseline)
#             # Calculate distance using the focal length of the right camera
#             distance_right = calculate_distance(disparity, focal_length_right, baseline)

#             # Print the calculated distances
#             print(f"Distance from Left Camera: {distance_left:.2f} meters")
#             print(f"Distance from Right Camera: {distance_right:.2f} meters")
#         else:
#             print("No disparity detected, distance cannot be calculated")

#     else:
#         print("Object not detected in both cameras")

#     # Show the frames
#     cv2.imshow('Left Camera', frame_left)
#     cv2.imshow('Right Camera', frame_right)

#     # Break the loop on 'q' key press
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the cameras and close windows
# cam_left.release()
# cam_right.release()
# cv2.destroyAllWindows()

import cv2
import numpy as np

def show_rectangle(img, x, y, w, h, window_name):
    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow(window_name, img)

class Stereocam:
    def __init__(self):
        self.centers = []

    def getContours(self, img):
        self.centers = []
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
        imgCanny = cv2.Canny(imgBlur, 50, 50)
        contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        bounding_boxes = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 100:  # Filter out small contours (you can adjust this threshold)
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                x, y, w, h = cv2.boundingRect(approx)
                center_x = x + (w / 2)
                center_y = y + (h / 2)
                self.centers.append((center_x, center_y))
                bounding_boxes.append((x, y, w, h))

        return bounding_boxes

# Capture from two cameras
img1 = cv2.VideoCapture(2)
img2 = cv2.VideoCapture(4)

camera1 = Stereocam()
camera2 = Stereocam()

fl1 = 0.06  # Focal length for camera 1
fl2 = 0.03  # Focal length for camera 2
camdis = 3  # Distance between the two cameras (adjust based on your setup)

while True:
    # Read frames from both cameras
    ref1, frame1 = img1.read()
    ref2, frame2 = img2.read()

    if not ref1 or not ref2:
        print("Failed to capture from one or both cameras")
        break

    # Get contours and bounding boxes from both cameras
    bounding_boxes1 = camera1.getContours(frame1)
    bounding_boxes2 = camera2.getContours(frame2)

    for i, (box1, center1) in enumerate(zip(bounding_boxes1, camera1.centers)):
        x1, y1, w1, h1 = box1
        show_rectangle(frame1, x1, y1, w1, h1, 'Camera 1')

        if i < len(camera2.centers):
            center2 = camera2.centers[i]
            disparity = abs(center1[0] - center2[0])
            if disparity != 0:
                distance1 = (fl1 * camdis) / disparity
                distance2 = (fl2 * camdis) / disparity
                print(f"Object {i+1} Distance from Camera 1: {distance1}")
                print(f"Object {i+1} Distance from Camera 2: {distance2}")
            else:
                print(f"Object {i+1} Distance: Infinite (Disparity is zero)")

    # Show rectangles in both camera windows
    for box2 in bounding_boxes2:
        x2, y2, w2, h2 = box2
        show_rectangle(frame2, x2, y2, w2, h2, 'Camera 2')

    # Display the results
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release camera resources and close windows
img1.release()
img2.release()
cv2.destroyAllWindows()

